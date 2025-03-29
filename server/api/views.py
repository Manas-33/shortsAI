import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .utils.youtube_utils import yt_downloader, get_yt_video_streams
from .utils.transcript_utils import get_transcript
from .utils.highlight_utils import get_highlight
from .utils.edit_utils import crop_clips
from django.conf import settings
import json
import cloudinary.uploader
import os


def hello_world(request):
    return JsonResponse({"message": "Hello World!"})

@csrf_exempt
def get_video_streams(request):
    if request.method == 'POST':
        url = json.loads(request.body)['url']
        if url:
            streams = get_yt_video_streams(url)
            return JsonResponse({"streams": streams})
        return JsonResponse({"error": "URL is required"}, status=400)
    return JsonResponse({"message": "Method not allowed!"}, status=405)

def formatted_transcript(transcript):
    if len(transcript) > 0:
        result = ""
        for text, start, end in transcript:
            result += (f"{start} - {end}: {text}")
        return result
    return ""

@csrf_exempt
def get_shorts(request):
    if request.method == 'POST':
        print(request.body)
        url = json.loads(request.body)['url']
        video_choice = int(json.loads(request.body)['video_choice'])
        if url:
            video, title = yt_downloader(url, video_choice)
            transcript = get_transcript(url)
            format_transcript = formatted_transcript(transcript)
            times = get_highlight(format_transcript)
            cloudinary_urls = []
            clips_dir = os.path.join(settings.BASE_DIR, 'api', 'clips/')
            i = 1
            for start, end in times:
                Output = f"{i}_{title}.mp4"
                clip_path = os.path.join(clips_dir, Output)
                crop_clips(video, Output, start, end)
                upload_result = cloudinary.uploader.upload(clip_path, resource_type="video")

                cloudinary_urls.append({
                    "clip_number": i,
                    "url": upload_result["secure_url"]
                })

                # os.remove(Output)
                i += 1
            
            return JsonResponse({
                "message": "Success",
                "video_path": video,
                "clips": cloudinary_urls
            })
        return JsonResponse({"error": "URL is required"}, status=400)
    return JsonResponse({"message": "Method not allowed!"}, status=405)

#  This code is purposefully left here for testing cloudinary without wasting openai credits 
# @csrf_exempt
# def get_shorts(request):
#     if request.method == 'POST':
#         try:
#             cloudinary_urls = []
#             clips_dir = os.path.join(settings.BASE_DIR, 'api', 'clips/')
#             print(clips_dir)
#             # Ensure the clips directory exists
#             if not os.path.exists(clips_dir):
#                 return JsonResponse({"error": "No clips found in './clips'"}, status=400)

#             i = 1
#             for file_name in os.listdir(clips_dir):
#                 if file_name.endswith(".mp4"):
#                     file_path = os.path.join(clips_dir, file_name)

#                     upload_result = cloudinary.uploader.upload(file_path, resource_type="video")

#                     cloudinary_urls.append({
#                         "clip_number": i,
#                         "url": upload_result["secure_url"]
#                     })

#                     os.remove(file_path)
#                     i += 1

#             return JsonResponse({
#                 "message": "Success",
#                 "clips": cloudinary_urls
#             })
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"message": "Method not allowed!"}, status=405)
