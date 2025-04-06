from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VideoProcessing
from .serializers import VideoProcessingSerializer, VideoRequestSerializer
from .tasks import process_video_task

# Create your views here.

class ShortsGeneratorView(APIView):
    """
    API endpoint to generate short videos from YouTube URLs
    """
    
    def post(self, request, format=None):
        serializer = VideoRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            url = serializer.validated_data['url']
            username = serializer.validated_data['username']
            num_shorts = serializer.validated_data.get('num_shorts', 1)
            
            # Create a new video processing record
            video_processing = VideoProcessing.objects.create(
                youtube_url=url,
                username=username,
                num_shorts=num_shorts,
                status='PENDING'
            )
            
            # Start processing using Celery
            process_video_task.delay(video_processing.id)
            
            # Return the processing record with a 202 Accepted status
            response_serializer = VideoProcessingSerializer(video_processing)
            return Response(
                {
                    'message': f'Video processing started for {num_shorts} shorts',
                    'processing': response_serializer.data
                }, 
                status=status.HTTP_202_ACCEPTED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VideoProcessingStatusView(APIView):
    """
    API endpoint to check the status of a video processing task
    """
    
    def get(self, request, processing_id, format=None):
        try:
            video_processing = VideoProcessing.objects.get(id=processing_id)
            serializer = VideoProcessingSerializer(video_processing)
            return Response(serializer.data)
        except VideoProcessing.DoesNotExist:
            return Response(
                {'error': 'Processing task not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class UserVideosView(APIView):
    """
    API endpoint to get all videos for a specific user
    """
    
    def get(self, request, username, format=None):
        videos = VideoProcessing.objects.filter(username=username)
        serializer = VideoProcessingSerializer(videos, many=True)
        return Response(serializer.data)
