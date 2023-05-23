from .models import *
from accounts.models import *
from itertools import chain

""" Helper functions """
def list_to_string(list):
	""" 
	Returns a list as string
	"""
	init_str = " "
	return(init_str.join(list))

def get_user_profile(user_id):
	""" 
	Returns the Profile object of the given user ID
	"""
	if user_id != None:
		profile = User.objects.get(id=user_id)
		return profile
	else:
		return None

def get_post_likes(post_id):
	""" 
	Returns the number of likes of the given post ID
	"""
	if post_id != None:
		post = user_feed_likes.objects.filter(post_id=post_id)
		return len(post)
	else:
		return None

def get_post_images(post_id):
	""" 
	Returns the images of the given post ID
	"""
	if post_id != None:
		if user_feed_images.objects.filter(post_id=post_id):
			images = user_feed_images.objects.filter(post_id=post_id)
			if len(images) > 1:
				for x in images:
					return x.image
			else:
				return images
		else:
			return None
	else:
		return None

def if_post_liked_by_user(user_id, post_id):
	""" 
	Returns True or False 
	If the post ID given is liked by the current user
	"""
	if user_id == None:
		return False
	elif post_id == None:
		return False
	else:
		post = user_feed_likes.objects.filter(post_id=post_id, by=user_id)
		if post:
			return True
		else:
			return False