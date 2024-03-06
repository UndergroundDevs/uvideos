from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=36)
    file = serializers.FileField(required=True)

    def save(self):
        # video = Video.save(title=self.validated_data["title"])
        print(self.validated_data)
