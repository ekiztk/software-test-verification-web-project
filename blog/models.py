from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class ImageUploadModel(models.Model):
    image = models.ImageField(upload_to='images/')

    # test 11 if image smaller than 5mb
    def clean(self):
        img = self.image
        if img:
            if img.size > 5*1024*1024:  # 5MB limit
                raise ValidationError("Image file too large ( > 5mb )")
        else:
            raise ValidationError("Couldn't read uploaded image")