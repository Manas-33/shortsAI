from django.shortcuts import render
from django.http import JsonResponse
from .utils.youtube_utils import yt_downloader, get_video_streams
from django.views.decorators.csrf import csrf_exempt
import json

def hello_world(request):
    return JsonResponse({"message": "Hello World!"})

@csrf_exempt
def get_video_streams(request):
    if request.method == 'POST':
        url = json.loads(request.body)['url']
        if url:
            streams = get_video_streams(url)
            return JsonResponse({"streams": streams})
        return JsonResponse({"error": "URL is required"}, status=400)
    return JsonResponse({"message": "Method not allowed!"}, status=405)

@csrf_exempt
def get_shorts(request):
    if request.method == 'POST':
        url = json.loads(request.body)['url']
        video_choice = int(json.loads(request.body)['video_choice'])
        if url:
            video = yt_downloader(url, video_choice)
            # WIP
            return JsonResponse({"message": "Success", "video_path": "video"})
        return JsonResponse({"error": "URL is required"}, status=400)
    return JsonResponse({"message": "Method not allowed!"}, status=405)