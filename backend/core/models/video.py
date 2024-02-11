from django.db import models


class Video(models.Model):
    id = models.CharField(max_length=36)
    path = models.CharField(max_length=255)
    digital_watermarking = models.BooleanField(default=False,  blank=True, null=False)
    published_date = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=False)
    deleted_at = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
