import os
from pytubefix import YouTube
import ffmpeg
import re

def get_video_size(stream):

    return stream.filesize / (1024 * 1024)

def sanitize_filename(filename):
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    sanitized = sanitized.replace(' ', '_')
    return sanitized

def download_youtube_video(url):
    try:
        yt = YouTube(url)

        video_streams = yt.streams.filter(type="video").order_by('resolution').desc()
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Automatically select the highest quality stream with reasonable size
        selected_stream = None
        # total = len(video_streams)
        # selected_stream = video_streams[total - 1]
        for stream in video_streams:
            size = get_video_size(stream)
            if size < 500:  # Less than 500 MB
                selected_stream = stream
                break
        
        # If no stream found with reasonable size, use the first one
        if not selected_stream and len(video_streams) > 0:
            selected_stream = video_streams[0]
        
        if not selected_stream:
            raise Exception("No suitable video stream found")

        if not os.path.exists('videos'):
            os.makedirs('videos')

        print(f"Downloading video: {yt.title}")
        video_file = selected_stream.download(output_path='videos', filename_prefix="video_")

        if not selected_stream.is_progressive:
            print("Downloading audio...")
            audio_file = audio_stream.download(output_path='videos', filename_prefix="audio_")
            sanitized_title = sanitize_filename(yt.title)
            print("Merging video and audio...")
            output_file = os.path.join('videos', f"{sanitized_title}.mp4")
            stream = ffmpeg.input(video_file)
            audio = ffmpeg.input(audio_file)
            stream = ffmpeg.output(stream, audio, output_file, vcodec='libx264', acodec='aac', strict='experimental')
            ffmpeg.run(stream, overwrite_output=True)

            os.remove(video_file)
            os.remove(audio_file)
        else:
            output_file = video_file

        
        print(f"Downloaded: {yt.title} to 'videos' folder")
        print(f"File path: {output_file}")
        return output_file

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ")
    download_youtube_video(youtube_url)
