import cv2
import numpy as np
from moviepy import *
from .face_detection_utils import detect_faces_and_speakers, Frames
import os
global Fps


def crop_to_vertical(input_video_path, output_video_path):
    try:
        # Check if input file exists
        if not os.path.exists(input_video_path):
            print(f"Error: Input video file not found: {input_video_path}")
            return False

        # Ensure output directory exists
        output_dir = os.path.dirname(output_video_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        detect_faces_and_speakers(input_video_path, "DecOut.mp4")
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(input_video_path, cv2.CAP_FFMPEG)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return False

        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        vertical_height = int(original_height)
        vertical_width = int(vertical_height * 9 / 16)
        print(vertical_height, vertical_width)

        if original_width < vertical_width:
            print("Error: Original video width is less than the desired vertical width.")
            return False

        x_start = (original_width - vertical_width) // 2
        x_end = x_start + vertical_width
        print(f"start and end - {x_start} , {x_end}")
        print(x_end-x_start)
        half_width = vertical_width // 2

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps,
                              (vertical_width, vertical_height))
        global Fps
        Fps = fps
        print(fps)
        count = 0
        for _ in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(faces) > -1:
                if len(faces) == 0:
                    # Check if we have frames data for this count
                    if count < len(Frames):
                        (x, y, w, h) = Frames[count]
                    else:
                        # If no frame data exists, use default cropping position
                        print(
                            f"No frame data for frame {count}, using default values")
                        x = x_start
                        y = 0
                        w = vertical_width
                        h = vertical_height

                # (x, y, w, h) = faces[0]
                try:
                    # check if face 1 is active
                    if count < len(Frames):
                        (X, Y, W, H) = Frames[count]
                    else:
                        # Default values if no face was detected for this frame
                        X = x_start
                        Y = 0
                        W = vertical_width
                        H = vertical_height
                except Exception as e:
                    print(e)
                    if count < len(Frames) and isinstance(Frames[count], list) and len(Frames[count]) > 0:
                        (X, Y, W, H) = Frames[count][0]
                        print(Frames[count][0])
                    else:
                        # Default values if error occurs
                        X = x_start
                        Y = 0
                        W = vertical_width
                        H = vertical_height

                for f in faces:
                    x1, y1, w1, h1 = f
                    center = x1 + w1//2
                    if center > X and center < X+W:
                        x = x1
                        y = y1
                        w = w1
                        h = h1
                        break

                # print(faces[0])
                centerX = x+(w//2)
                print(centerX)
                print(x_start - (centerX - half_width))
                if count == 0 or (x_start - (centerX - half_width)) < 1:
                    # IF dif from prev fram is low then no movement is done
                    pass  # use prev vals
                else:
                    x_start = centerX - half_width
                    x_end = centerX + half_width

                    if 'cropped_frame' in locals():  # Check if cropped_frame exists
                        if int(cropped_frame.shape[1]) != x_end - x_start:
                            if x_end < original_width:
                                x_end += int(cropped_frame.shape[1]
                                             ) - (x_end-x_start)
                                if x_end > original_width:
                                    x_start -= int(cropped_frame.shape[1]
                                                   ) - (x_end-x_start)
                            else:
                                x_start -= int(cropped_frame.shape[1]
                                               ) - (x_end-x_start)
                                if x_start < 0:
                                    x_end += int(cropped_frame.shape[1]
                                                 ) - (x_end-x_start)
                            print("Frame size inconsistant")
                            print(x_end - x_start)

            count += 1
            # Ensure x_start and x_end are valid
            x_start = max(0, min(original_width - vertical_width, x_start))
            x_end = min(original_width, x_start + vertical_width)

            cropped_frame = frame[:, x_start:x_end]
            if cropped_frame.shape[1] == 0:
                x_start = (original_width - vertical_width) // 2
                x_end = x_start + vertical_width
                cropped_frame = frame[:, x_start:x_end]

            print(cropped_frame.shape)

            out.write(cropped_frame)

        out.release()
        cap.release()
        cv2.destroyAllWindows()
        print(f"Vertical video saved as {output_video_path}")
        return True

    except Exception as e:
        print(f"Error in crop_to_vertical: {str(e)}")
        return False


def combine_videos(video_with_audio, video_without_audio, output_filename):
    try:
        # Check if input files exist
        if not os.path.exists(video_with_audio):
            print(f"Error: Audio source file not found: {video_with_audio}")
            return False

        if not os.path.exists(video_without_audio):
            print(f"Error: Video source file not found: {video_without_audio}")
            return False

        # Ensure output directory exists
        output_dir = os.path.dirname(output_filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Load video clips
        clip_with_audio = VideoFileClip(video_with_audio)
        clip_without_audio = VideoFileClip(video_without_audio)

        audio = clip_with_audio.audio

        combined_clip = clip_without_audio.set_audio(audio)

        global Fps
        combined_clip.write_videofile(
            output_filename, codec='libx264', audio_codec='aac', fps=Fps, preset='medium', bitrate='3000k')
        print(f"Combined video saved successfully as {output_filename}")
        return True

    except Exception as e:
        print(f"Error combining video and audio: {str(e)}")
        return False


if __name__ == "__main__":
    input_video_path = r'Out.mp4'
    output_video_path = 'Croped_output_video.mp4'
    final_video_path = 'final_video_with_audio.mp4'
    detect_faces_and_speakers(input_video_path, "DecOut.mp4")
    crop_to_vertical(input_video_path, output_video_path)
    combine_videos(input_video_path, output_video_path, final_video_path)
