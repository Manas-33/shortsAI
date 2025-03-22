import os
from pytubefix import YouTube
import ffmpeg
import re
import ssl

# for macos
def fix_ssl_certificate():
    # Create unverified SSL context to work around certificate issues
    ssl._create_default_https_context = ssl._create_unverified_context
    print("SSL certificate verification disabled for YouTube downloads")


def get_video_size(stream):
    return stream.filesize / (1024 * 1024)


def sanitize_filename(filename):
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    return sanitized


def get_video_streams(url):
    try:
        fix_ssl_certificate()
        yt = YouTube(url)
        video_streams = yt.streams.filter(
            type="video").order_by('resolution').desc()
        streams_info = []

        for i, stream in enumerate(video_streams):
            size = get_video_size(stream)
            stream_type = "Progressive" if stream.is_progressive else "Adaptive"
            streams_info.append({
                "index": i,
                "resolution": stream.resolution,
                "size": f"{size:.2f}",
                "type": stream_type,
                "fps": stream.fps
            })
        return streams_info
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


def yt_downloader(url, video_choice):
    try:
        # for macos
        fix_ssl_certificate()
        yt = YouTube(url)
        video_streams = yt.streams.filter(
            type="video").order_by('resolution').desc()
        audio_stream = yt.streams.filter(only_audio=True).first()

        selected_stream = video_streams[video_choice]

        videos_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'videos')
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        yt_title = yt.title
        print(f"Downloading video: {yt_title}")
        video_file = selected_stream.download(
            output_path=videos_dir, filename_prefix="video_")

        if not selected_stream.is_progressive:
            print("Downloading audio...")
            audio_file = audio_stream.download(
                output_path=videos_dir, filename_prefix="audio_")

            print("Merging video and audio...")
            sanitized_title = sanitize_filename(yt.title)
            output_file = os.path.join(videos_dir, f"{sanitized_title}.mp4")
            stream = ffmpeg.input(video_file)
            audio = ffmpeg.input(audio_file)
            stream = ffmpeg.output(
                stream, audio, output_file, vcodec='libx264', acodec='aac', strict='experimental')
            ffmpeg.run(stream, overwrite_output=True)

            os.remove(video_file)
            os.remove(audio_file)
        else:
            output_file = video_file
            sanitized_title = sanitize_filename(yt.title)
            new_output_file = os.path.join(
                videos_dir, f"{sanitized_title}.mp4")
            if os.path.exists(new_output_file):
                os.remove(new_output_file)
            os.rename(output_file, new_output_file)
            output_file = new_output_file

        print(f"Downloaded: {yt_title} to '{videos_dir}' folder")
        print(f"File path: {output_file}")
        return output_file, yt_title

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure you have the latest version of pytube and ffmpeg-python installed.")
        print("You can update them by running:")
        print("pip install --upgrade pytube ffmpeg-python")
        print("Also, ensure that ffmpeg is installed on your system and available in your PATH.")
