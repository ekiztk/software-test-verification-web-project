from django.conf import settings
from django.db import models
from django.utils import timezone

class ImageUploadModel(models.Model):
    image = models.ImageField(upload_to='images/')