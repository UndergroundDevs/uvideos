from rest_framework import serializers
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    valid_extensions = [
        '.mp4'
        # '.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls'
    ]
    ext = "." + value.name.split('.')[-1].lower()

    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}")


class VideoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=36)
    file = serializers.FileField(required=True, validators=[validate_file_extension])


class VideoValidateSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, validators=[validate_file_extension])


class VideoListSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    title = serializers.CharField(max_length=36)
    url = serializers.CharField(max_length=36)
    digital_watermarking = serializers.BooleanField()
    published_date = serializers.DateTimeField()
