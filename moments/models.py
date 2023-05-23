from django.db import models
from accounts.models import *
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class Moment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('created_at',)

def get_image_filename(instance, filename):
    moment_id = instance.moment.id
    return "contents/moments/%s/%s" % (moment_id, filename)

class MomentImages(models.Model):
    moment = models.ForeignKey(Moment, default=None, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='moment_images', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
