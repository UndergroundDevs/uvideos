from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from video.serializers import VideoSerializer
from rest_framework import status


class VideoView(APIView):
    video_serializer: VideoSerializer = VideoSerializer

    def post(self, request: Request):
        serializer = self.video_serializer(data=request.data)

        # print(serializer.is_valid())
        # print(serializer.error_messages)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": ["Arquivo carregado com sucesso"]})

        return JsonResponse({"message": serializer.error_messages}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
