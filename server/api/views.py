import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .utils.youtube_utils import yt_downloader, get_video_streams
from .utils.transcript_utils import get_transcript
from .utils.highlight_utils import get_highlight
from .utils.edit_utils import crop_clips


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
        url = json.loads(request.body)['url']
        video_choice = int(json.loads(request.body)['video_choice'])
        if url:
            video, title = yt_downloader(url, video_choice)
            transcript = get_transcript(url)
            format_transcript = formatted_transcript(transcript)
            times = get_highlight(format_transcript)
            i = 1
            for start, end in times:
                Output = f"{i}_{title}.mp4"
                crop_clips(video, Output, start, end)
                i += 1
            return JsonResponse({"message": "Success", "video_path": video, "clips": len(times)})
        return JsonResponse({"error": "URL is required"}, status=400)
    return JsonResponse({"message": "Method not allowed!"}, status=405)
