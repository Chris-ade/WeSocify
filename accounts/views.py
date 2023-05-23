from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from feed.models import *
from .forms import *
from .utils import *

def register(request):
  if request.user.is_authenticated:
    return redirect(reverse('feed:home'))
  else:
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['cpassword']
        birth_date = request.POST['birth_date']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'An account with that e-mail already exists')
                return redirect(reverse('accounts:register'))
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'The username has been taken, try another')
                return redirect(reverse('accounts:register'))
            else:
                user = User.objects.create_user(username=username, name=name, email=email, password=password, birth_date=birth_date)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect(reverse('accounts:settings'))
        else:
            messages.info(request, 'The password does not match')
            return redirect(reverse('accounts:welcome'))
    else:
        return render(request, 'welcome/register.html', {'page_title': "Register an account"})

def welcome(request):
  if request.user.is_authenticated:
    return redirect(reverse('feed:home'))
  else:
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('feed:home'))
            else:
                form = login_form(initial={'username': username, 'password': password})
                return render(request, 'welcome/content.html', {'page_title': "Welcome", 'form': form, 'error': 'Invalid credentials'})
        else:
            form = login_form(initial={'username': username, 'password': password})
            return render(request, 'welcome.html', {'page_title': "Welcome", 'form': form})
    else:
        form = login_form()
        return render(request, 'welcome/content.html', {'page_title': "Welcome", 'form': form})

def terms(request):
    return render(request, 'welcome/terms.html')

def privacy_policy(request):
    return render(request, 'welcome/privacy-policy.html')

@login_required
def logout(request):
  if request.user.is_authenticated:
    auth.logout(request)
    response = HttpResponse()
    response['HX-Redirect'] = reverse("accounts:welcome")
    return redirect(reverse('accounts:welcome'))

@login_required
def get(request, username):
  '''
    Retrieve information about a user and render it in a template.

    Args:
        request (object): the HTTP request object
        username: (string): the username of the user to be retrieved

    Returns:
        A rendered template displaying information about the specified user, or a 404 error page if the user does not exist.
    Example:
        GET /johndoe/
  '''
  try:
      user_object = User.objects.get(username=username)
      user_posts = Feed.objects.filter(user__username=username)
      context = {
        'page_title': f'{user_object.name} (@{user_object.username})',
        'user': user_object,
        'user_posts': user_posts,
        'user_post_count': user_posts.count(),
        'user_followers': user_object.followers.all,
        'user_following': user_object.following.all,
      }
      return render(request, 'profile/content.html', context)
  except User.DoesNotExist:
      return render(request, 'errors/404.html')

@login_required
def feeds(request, username):
  '''
    Displays all the feeds created by a user.
    
    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose feeds are to be displayed.
        
    Returns:
        HttpResponse: A rendered template displaying the feeds created by the user. If the user does not exist, returns a "404 Not Found" response.

    Example:
        GET /johndoe/feeds/
  '''
  try:
    user_obj = User.objects.get(username=username)
    feed_obj = Feed.objects.filter(user__username=username).order_by('-created_at')
    context = {
      'feeds': feed_obj,
      'user': user_obj
    }
    return render(request, 'profile/feeds/content.html', context)
  except User.DoesNotExist:
    return HttpResponse("Not Found", status = 404)

@login_required
def with_replies(request, username):
  '''
    Displays all the feeds created by a user that have received replies.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose feeds are to be displayed.

    Returns:
        HttpResponse: A rendered template displaying the feeds created by the user that have replies. If the user does not exist, returns a "404 Not Found" response.

    Example:
        GET /johndoe/with_replies/
  '''
  try:
    user_obj = User.objects.get(username=username)
    feed_obj = Feed.objects.filter(
    user__username=username,
    comments__user__username=username).distinct().order_by('-created_at')
    context = {
      'feeds': feed_obj,
      'user': user_obj
    }
    return render(request, 'profile/feeds/with_replies.html', context)
  except User.DoesNotExist:
    return HttpResponse("Not Found", status = 404)

@login_required
def media(request, username):
  '''
    Displays all the media created by a user.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose media are to be displayed.

    Returns:
        HttpResponse: A rendered template displaying the media created by the user. If the user does not exist, returns a "404 Not Found" response.

    Example:
        GET /johndoe/media/
  '''
  try:
    user_obj = User.objects.get(username=username)
    feeds = Feed.objects.filter(user__username=username, images__isnull=False).prefetch_related('images').order_by('-created_at')
    context = {
      'feeds': feeds,
      'user': user_obj
    }
    return render(request, 'profile/feeds/media.html', context)
  except User.DoesNotExist:
    return HttpResponse("Not Found", status=404)

@login_required
def likes(request, username):
  '''
    Displays all the feeds that a user has liked.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the user whose liked feeds are to be displayed.

    Returns:
        HttpResponse: A rendered template displaying the liked feeds of the user. If the user does not exist, returns a "404 Not Found" response.

    Example:
        GET /johndoe/likes/
  '''
  try:
    user_obj = User.objects.get(username=username)
    feed_obj = Feed.objects.filter(likes__username=username).order_by('-created_at')
    context = {
      'feeds': feed_obj,
      'user': user_obj
    }
    return render(request, 'profile/feeds/likes.html', context)
  except User.DoesNotExist:
    return HttpResponse("Not Found", status = 404)

@login_required
def follow(request, user):
  '''
    Follow or unfollow a user
    Args:
        request: The request object
        user: The username of the user to follow or unfollow
    Returns:
        redirect: Redirects the user to the profile page of the user they are following or unfollowing
  '''
  user = User.objects.get(username=user)
  current_user = request.user
  following = user.followers.all()
  if user.username != current_user.username:
    if current_user in following:
      user.followers.remove(current_user.id)
    else:
      user.followers.add(current_user.id)
  return redirect(reverse('accounts:profile', args=[user]))

@login_required
def followers(request, username):
  '''Users Followers
  
  Note:
      Fetch all the accounts following the user.
      
  Args:
      request (object): The current request object containing details about the current logged on user's session.
      username (str): The user's username.

  Returns:
      HttpResponse (object): Returns a page containing all the accounts.
  '''
  user_object = User.objects.get(username=username)
  followers = user_object.followers.all
  following = user_object.following.all
  context = {
    'page_title': "Followers",
    'user': user_object,
    'followers': followers,
    'following': following
  }
  return render(request, 'profile/followers/content.html', context)

@login_required
def following(request, username):
  '''Users Following
  
  Note:
      Fetch all the accounts the user is following.
      
  Args:
      request (object): The current request object containing details about the current logged on user's session.
      username (str): The user's username.

  Returns:
      HttpResponse (object): Returns a page containing all the accounts.
  '''
  user_object = User.objects.get(username=username)
  followers = user_object.followers.all
  following = user_object.following.all
  context = {
    'page_title': "Following",
    'user': user_object,
    'followers': followers,
    'following': following
  }
  return render(request, 'profile/following/content.html', context)

@login_required
def settings(request):
  '''User profile settings
  
  Note:
      Fetch the current user account data.
      If the request method is POST, updates the user's data in regards to the submitted form.
      
  Args:
      request (object): The current request object containing details about the current logged on user's session.

  Returns:
      HttpResponse (object): Returns a page containing a form filled with the current user account data.
  '''
  user = request.user
  if request.method != 'POST':
    data = {
      'bio': user.bio, 
      'location': user.location,
      'website': user.website
    }
    context = {
      'page_title': "Settings",
      'user_profile': user,
      'form': settings_form(initial=data)
    }
    return render(request, 'profile/settings/content.html', context)
  form = settings_form(request.POST, request.FILES)
  if form.is_valid():
    bio = form.cleaned_data['bio']
    location = form.cleaned_data['location']
    website = form.cleaned_data['website']
    avatar = request.FILES.get('avatar', None)
    cover = request.FILES.get('cover', None)
    birth_date = request.POST.get('birth_date')
    if avatar is not None:
      user.avatar = avatar
    if cover is not None:
      user.cover = cover
    user.bio = bio
    user.location = location
    user.website = website
    # user.birth_date = birth_date
    user.save()
    return redirect(reverse('accounts:settings'))