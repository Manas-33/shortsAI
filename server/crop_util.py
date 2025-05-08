import cv2
import numpy as np
import mediapipe as mp
import os
import argparse
from tqdm import tqdm

class FaceTrackingVideoCropper:
    def __init__(self, output_width=1080, output_height=1920):

        self.output_width = output_width
        self.output_height = output_height
        self.aspect_ratio = self.output_width / self.output_height
        
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )
        
    def detect_faces(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(frame_rgb)
        
        faces = []
        if results.detections:
            img_height, img_width, _ = frame.shape
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * img_width)
                y = int(bbox.ymin * img_height)
                w = int(bbox.width * img_width)
                h = int(bbox.height * img_height)
                faces.append((x, y, w, h))
                
        return faces
    
    def calculate_crop_region(self, frame, faces, padding_factor=1.5):
        if not faces:
            # If no faces detected, use the center of the frame
            img_height, img_width, _ = frame.shape
            target_width = min(img_width, int(img_height * self.aspect_ratio))
            x = (img_width - target_width) // 2
            return x, 0, target_width, img_height
        
        # Calculate the center point of all faces
        centers_x = []
        centers_y = []
        for x, y, w, h in faces:
            centers_x.append(x + w // 2)
            centers_y.append(y + h // 2)
        
        center_x = sum(centers_x) // len(centers_x)
        center_y = sum(centers_y) // len(centers_y)
        
        # Calculate the maximum distance from center to include all faces with padding
        max_dist_x = 0
        max_dist_y = 0
        for x, y, w, h in faces:
            max_dist_x = max(max_dist_x, abs(center_x - x), abs(center_x - (x + w)))
            max_dist_y = max(max_dist_y, abs(center_y - y), abs(center_y - (y + h)))
        
        # Apply padding
        crop_width = int(max_dist_x * 2 * padding_factor)
        crop_height = int(max_dist_y * 2 * padding_factor)
        
        # Adjust to maintain aspect ratio
        img_height, img_width, _ = frame.shape
        
        if crop_width / crop_height > self.aspect_ratio:
            # Too wide, adjust height
            crop_height = int(crop_width / self.aspect_ratio)
        else:
            # Too tall, adjust width
            crop_width = int(crop_height * self.aspect_ratio)
        
        # Calculate the top-left corner of the crop region
        x = max(0, center_x - crop_width // 2)
        y = max(0, center_y - crop_height // 2)
        
        # Ensure the crop region fits within the frame
        if x + crop_width > img_width:
            x = img_width - crop_width
        if y + crop_height > img_height:
            y = img_height - crop_height
            
        # If crop dimensions are still out of bounds, adjust them
        if x < 0:
            x = 0
            crop_width = min(img_width, crop_width)
        if y < 0:
            y = 0
            crop_height = min(img_height, crop_height)
        
        return x, y, crop_width, crop_height
    
    def apply_smoothing(self, crop_regions, window_size=15):
        smoothed_regions = []
        
        # If no regions, return empty list
        if not crop_regions:
            return smoothed_regions
            
        # Initialize with the first crop region
        prev_smooth_x, prev_smooth_y = crop_regions[0][0], crop_regions[0][1]
        prev_smooth_w, prev_smooth_h = crop_regions[0][2], crop_regions[0][3]
        
        # Parameters for exponential smoothing
        alpha_position = 0.08  # Smoothing factor for position (smaller = smoother)
        alpha_size = 0.05      # Smoothing factor for size (smaller = smoother)
        
        # Parameters for adaptive smoothing based on movement speed
        max_speed_threshold = 30  # Maximum pixel movement before reducing smoothing
        
        for i in range(len(crop_regions)):
            x, y, w, h = crop_regions[i]
            
            # Calculate the movement speed from previous frame
            if i > 0:
                dx = abs(x - crop_regions[i-1][0])
                dy = abs(y - crop_regions[i-1][1])
                speed = dx + dy
                
                # Adjust smoothing based on speed (faster movement = less smoothing)
                current_alpha_position = min(0.5, alpha_position * (1 + (speed / max_speed_threshold)))
            else:
                current_alpha_position = alpha_position
            
            # Apply exponential smoothing for position
            smooth_x = int(current_alpha_position * x + (1 - current_alpha_position) * prev_smooth_x)
            smooth_y = int(current_alpha_position * y + (1 - current_alpha_position) * prev_smooth_y)
            
            # Apply stronger smoothing for size to prevent "breathing" effect
            smooth_w = int(alpha_size * w + (1 - alpha_size) * prev_smooth_w)
            smooth_h = int(alpha_size * h + (1 - alpha_size) * prev_smooth_h)
            
            # Update previous values for next iteration
            prev_smooth_x, prev_smooth_y = smooth_x, smooth_y
            prev_smooth_w, prev_smooth_h = smooth_w, smooth_h
            
            smoothed_regions.append((smooth_x, smooth_y, smooth_w, smooth_h))
        
        # Apply additional window-based smoothing for extra stability
        final_smoothed = []
        for i in range(len(smoothed_regions)):
            # Calculate the valid range for the smoothing window
            effective_window = min(window_size, len(smoothed_regions))
            start_idx = max(0, i - effective_window // 2)
            end_idx = min(len(smoothed_regions), i + effective_window // 2 + 1)
            window = smoothed_regions[start_idx:end_idx]
            
            # Apply weighted averaging with center frames having more weight
            weights = [1 - abs(i - j) / effective_window for j in range(start_idx, end_idx)]
            total_weight = sum(weights)
            
            # Calculate weighted averages
            x_avg = sum(weights[j-start_idx] * window[j-start_idx][0] for j in range(start_idx, end_idx)) / total_weight
            y_avg = sum(weights[j-start_idx] * window[j-start_idx][1] for j in range(start_idx, end_idx)) / total_weight
            w_avg = sum(weights[j-start_idx] * window[j-start_idx][2] for j in range(start_idx, end_idx)) / total_weight
            h_avg = sum(weights[j-start_idx] * window[j-start_idx][3] for j in range(start_idx, end_idx)) / total_weight
            
            final_smoothed.append((int(x_avg), int(y_avg), int(w_avg), int(h_avg)))
        
        return final_smoothed
    
    def process_video(self, input_path, output_path, smoothing_window=30, padding_factor=1.6):
        # Open the input video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {input_path}")
            return
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Collect all crop regions first
        print("Analyzing video frames and detecting faces...")
        crop_regions = []
        
        for _ in tqdm(range(frame_count)):
            ret, frame = cap.read()
            if not ret:
                break
                
            faces = self.detect_faces(frame)
            crop_region = self.calculate_crop_region(frame, faces, padding_factor)
            crop_regions.append(crop_region)
        
        # Apply smoothing to the crop regions
        print("Applying smoothing to camera movement...")
        smoothed_regions = self.apply_smoothing(crop_regions, smoothing_window)
        
        # Reset the video capture
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # Create the output video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (self.output_width, self.output_height))
        
        # Process the video again and write the output frames
        print("Creating output video...")
        frame_idx = 0
        
        for _ in tqdm(range(frame_count)):
            ret, frame = cap.read()
            if not ret:
                break
                
            x, y, w, h = smoothed_regions[frame_idx]
            
            # Crop the frame
            try:
                # Make sure crop region is within bounds
                img_height, img_width, _ = frame.shape
                x = max(0, min(x, img_width - 10))
                y = max(0, min(y, img_height - 10))
                w = min(w, img_width - x)
                h = min(h, img_height - y)
                
                cropped_frame = frame[y:y+h, x:x+w]
                
                # Resize to output dimensions
                resized_frame = cv2.resize(cropped_frame, (self.output_width, self.output_height))
                
                # Write the frame
                out.write(resized_frame)
            except Exception as e:
                print(f"Error processing frame {frame_idx}: {e}")
                # Use the whole frame if there's an error
                resized_frame = cv2.resize(frame, (self.output_width, self.output_height))
                out.write(resized_frame)
            
            frame_idx += 1
        
        # Release resources
        cap.release()
        out.release()
        print(f"Done! Output saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Face Tracking Video Cropper for Shorts")
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("output", help="Output video file path")
    parser.add_argument("--width", type=int, default=1080, help="Output video width (default: 1080)")
    parser.add_argument("--height", type=int, default=1920, help="Output video height (default: 1920)")
    parser.add_argument("--smooth", type=int, default=30, help="Smoothing window size (default: 30)")
    parser.add_argument("--padding", type=float, default=1.6, help="Padding factor around faces (default: 1.6)")
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist")
        return
    
    # Create the face tracking video cropper
    cropper = FaceTrackingVideoCropper(args.width, args.height)
    
    # Process the video
    cropper.process_video(args.input, args.output, args.smooth, args.padding)

if __name__ == "__main__":
    main()