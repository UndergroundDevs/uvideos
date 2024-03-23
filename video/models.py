from django.db import models
import uuid


class Video(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    title = models.CharField(max_length=36, null=False, blank=False)
    path = models.CharField(max_length=36, null=False, blank=False)
    digital_watermarking = models.BooleanField(default=False,  blank=True, null=False)
    published_date = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=False)
    deleted_at = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.path

    class Meta:
        db_table = "VIDEO"
