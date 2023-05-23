from .models import *
from feed.models import *

""" Helper functions """

def get_account_followers(obj):
    user_followers = obj.followers.all()
    followers = [follow.id for follow in user_followers]
    return followers

def get_account_following(obj):
    user_following = obj.following.all()
    following = [follow.id for follow in user_following]
    return following

def get_username(obj):
	return obj.username