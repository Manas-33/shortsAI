from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy import VideoFileClip
import os

def crop_clips(input_file, output_file, start_time, end_time):
    with VideoFileClip(input_file) as video:
        cropped_video = video.subclipped(start_time, end_time)
        output_directory = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'clips')
        os.makedirs(output_directory, exist_ok=True)
        output_file = os.path.join(output_directory, output_file)
        cropped_video.write_videofile(output_file, codec='libx264')
