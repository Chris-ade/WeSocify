from django.db import models
from accounts.models import *
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

def get_image_filename(instance, filename):
    feed_id = instance.feed.id
    return "contents/feed/%s/%s" % (feed_id, filename)

def get_comment_image_filename(instance, filename):
    comment_id = instance.comment.id
    return "contents/comment/%s/%s" % (comment_id, filename)

class Feed(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name="feed_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
      return self.text
    
    def follower_comment(self):
      followers = self.user.user_followers()
      return self.comments.filter(user__username__in=followers).first()
    
    def poll(self):
      try:
        poll = Poll.objects.get(feed__id=self.id)
        return poll
      except Poll.DoesNotExist:
        return None
    
    def is_reposted(self):
      try:
        repost = Repost.objects.get(feed__id=self.id)
        return True
      except Repost.DoesNotExist:
        return False
    
    def reposted_by(self):
      try:
        repost = Repost.objects.get(feed__id=self.id)
        return repost.by
      except Repost.DoesNotExist:
        return None
    
    class Meta:
        ordering = ('created_at',)

class Poll(models.Model):
    feed = models.ForeignKey(Feed, default=None, related_name="feed_poll", on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
      return self.feed.text
    
    def users_voted(self):
      votes = Vote.objects.filter(choice__poll__id=self.id)
      votes_list = [vote.user for vote in votes]
      return votes_list
    
    def votes_count(self):
      count = Vote.objects.filter(choice__poll__id=self.id).count()
      return count

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name="choices", default=None, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
      return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name="poll_votes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_voted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
      return self.choice.choice_text
    
class FeedMedia(models.Model):
    feed = models.ForeignKey(Feed, default=None, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='feed_images', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, default=None, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)

class CommentMedia(models.Model):
    comment = models.ForeignKey(Comments, default=None, related_name="comment_image", on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, default=None, related_name="comment_image", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_comment_image_filename, verbose_name='comment_images', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Repost(models.Model):
    feed = models.ForeignKey(Feed, default=None, related_name="repost", on_delete=models.CASCADE)
    by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)