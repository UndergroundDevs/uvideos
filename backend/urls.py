"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .settings import MEDIA_ROOT, MEDIA_URL
from django.urls import path
from video.views import VideoListView, VideoDetailView, VideoValidateDigitalWaterMark
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('video/', VideoListView.as_view()),
    path('video/validate/', VideoValidateDigitalWaterMark.as_view()),
    path('video/<str:pk>/', VideoDetailView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
