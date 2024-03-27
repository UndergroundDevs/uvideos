from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from video.serializers import VideoSerializer, VideoListSerializer, VideoValidateSerializer
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from .models import Video
from uuid import uuid4
from rest_framework.exceptions import NotFound
from dwm import DigitalWaterMark
import os


class VideoListView(APIView):
    video_serializer: VideoSerializer = VideoSerializer

    def post(self, request: Request):
        serializer = self.video_serializer(data=request.data)
        file_system = FileSystemStorage()

        if serializer.is_valid():
            try:
                file_name: str = file_system.save(f"{uuid4()}-{request.data['file'].name}", request.data["file"])
                digital_watermarking_id = uuid4()
                video = Video(title=request.data["title"], path=file_name,
                              digital_watermarking_id=digital_watermarking_id,
                              digital_watermarking=True)
                dwm = DigitalWaterMark()
                print(os.path.join(
                                        os.path.dirname(os.path.abspath(__file__)),
                                                  # "media", "..",
                                                  file_name))
                dwm.encode_video(os.path.join("media", file_name), f"{digital_watermarking_id}",
                                 10,
                                 os.path.join(
                                        os.path.dirname(os.path.abspath(__file__)),
                                                  # "media",
                                     "..", "media", file_name))
                video.save()
                return JsonResponse({"message": ["Arquivo carregado com sucesso"]})
            except:
                return JsonResponse({"message": ["Failed to add digital watermark to video"]},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
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


class VideoValidateDigitalWaterMark(APIView):
    video_serializer: VideoValidateSerializer = VideoValidateSerializer

    def validate_video(self, digital_watermarking_id):
        try:
            return Video.objects.get(digital_watermarking_id=digital_watermarking_id)
        except Video.DoesNotExist:
            raise NotFound(detail={"message": ["Invalid video"]}, code=None)

    def post(self, request: Request):
        """
        :type request: Request
        :type pk: basestring
        """
        serializer = self.video_serializer(data=request.data)
        file_system = FileSystemStorage()

        if serializer.is_valid():
            file_name = file_system.save(f"{uuid4()}-{request.data['file'].name}", request.data["file"])
            dwm = DigitalWaterMark()
            digital_watermarking_id = None

            try:
                digital_watermarking_id = dwm.decode_video(os.path.join("media", file_name), 10)
            except:
                return JsonResponse({"message": ["Invalid video"]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            video = self.validate_video(digital_watermarking_id)
            video.url = "http://localhost:8000" + "/media/" + video.path
            video_list_serialized = VideoListSerializer(video)

            return JsonResponse({
                "message": ["Video validated successfully"],
                "video": video_list_serialized.data
            })

        return JsonResponse({"message": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


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
