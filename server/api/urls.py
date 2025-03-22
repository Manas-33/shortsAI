from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('streams/', views.fetch_video_streams, name='fetch_video_streams'),
    path('shorts/', views.get_shorts, name='get_shorts'),
]
