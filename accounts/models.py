from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

def get_image_filename(instance, filename):
    user_id = instance.id
    return f"contents/avatars/{user_id}/{filename}"

def get_cover_image_filename(instance, filename):
    user_id = instance.id
    return f"contents/covers/{user_id}/ {filename}"

class User(AbstractUser):
    """ 
    The model class responsible for handling users
    """
    first_name = None
    last_name = None
    name = models.TextField(max_length=50)
    bio = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to=get_image_filename, default='default.png')
    cover = models.ImageField(upload_to=get_cover_image_filename, default='default_cover.jpg')
    location = models.CharField(max_length=30, blank=True)
    website = models.CharField(max_length=100, blank=True)
    followers = models.ManyToManyField(
        "self", blank=True, related_name="following", symmetrical=False
    )
    birth_date = models.DateField()

    def user_followers(self):
      user_followers = self.followers.all()
      followers = [follow.username for follow in user_followers]
      return followers
    
    def user_following(self):
      user_following = self.following.all()
      following = [follow.username for follow in user_following]
      return following

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username