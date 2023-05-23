from django.contrib import admin
from .models import *
"""
class FeedAdmin(admin.ModelAdmin):
	model = user_feed
	fields = ['user', 'username', 'text', 'likes']

class FeedImagesAdmin(admin.ModelAdmin):
	model = user_feed_images
	fields = ['post', 'image']

admin.site.register(user_feed, FeedAdmin)
admin.site.register(user_feed_images, FeedImagesAdmin)
"""