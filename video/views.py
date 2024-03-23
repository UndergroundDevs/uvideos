from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from video.serializers import VideoSerializer, VideoListSerializer
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from .models import Video
from uuid import uuid4
from rest_framework.exceptions import NotFound


class VideoListView(APIView):
    video_serializer: VideoSerializer = VideoSerializer

    def post(self, request: Request):
        serializer = self.video_serializer(data=request.data)
        file_system = FileSystemStorage()

        if serializer.is_valid():
            file_name = file_system.save(f"{uuid4()}-{request.data['file'].name}", request.data["file"])
            video = Video(title=request.data["title"], path=file_name, digital_watermarking=False)
            video.save()
            return JsonResponse({"message": ["Arquivo carregado com sucesso"]})
        return JsonResponse({"message": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        video = Video.objects.all()
        for item in video:
            item.url = "http://localhost:8000" + "/media/" + item.path

        video_list_serialized = VideoListSerializer(video, many=True)

        return JsonResponse({
            "message": ["Lista de arquivos carraegada com sucesso"],
            "video": video_list_serialized.data
        })


class VideoDetailView(APIView):
    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise NotFound(detail={"message": "Video not found"}, code=None)

    def get(self, request, pk):
        """
        :type request: Request
        :type pk: basestring
        """
        video = self.get_object(pk)
        video.url = "http://localhost:8000" + "/media/" + video.path
        video_list_serialized = VideoListSerializer(video)

        return JsonResponse({
            "message": ["Lista de arquivos carraegada com sucesso"],
            "video": video_list_serialized.data
        }, status=status.HTTP_200_OK)
