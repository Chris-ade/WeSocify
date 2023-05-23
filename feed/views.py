from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.models import *
from moments.models import *
from .models import *
from .forms import *
from .utils import *
from itertools import chain
import json

@never_cache
@login_required
def compose(request):
  context = {
    'page_title': "Compose Feed",
    'post_form': PostForm(),
    'poll_form': ChoiceFormSet(),
    'poll_hours': range(24),
    'poll_minutes': range(60),
  }
  return render(request, 'feed/compose/content.html', context)

@never_cache
@login_required
def view(request, username, pk):
  try:
    feed_object = Feed.objects.get(pk=pk)
    user_object = request.user
    followers = feed_object.user.user_followers()
    context = {
      'page_title': "Feed",
      'user_profile': user_object,
      'post': feed_object,
      'followers': followers
    }
    return render(request, 'feed/view.html', context)
  except Feed.DoesNotExist:
    return render(request, 'errors/404.html')

@never_cache
@login_required
def home(request):
  try:
    feed_object = get_user_feed(request)
    feed, page, total_pages = pagination(request, feed_object)
    user_following = request.user.user_followers()
    user_object = request.user
    current_page = int(request.POST.get('page', 1))
    context = {
      'page_title': "Home",
      'post_form': PostForm(),
      'user_profile': user_object,
      'following': user_following,
      'page': page,
      'total_pages': total_pages,
      'posts': feed
    }
    return render(request, 'feed/content.html', context)
  except Feed.DoesNotExist:
    return render(request, 'feed/content.html', context)

@login_required
def suggestions(request):
    obj = get_user_suggestions(request)
    context = {
      'suggestions': obj[:4]
    }
    return render(request, 'feed/suggestions.html', context)

@login_required
def vote(request):
    if request.method != 'POST':
        return JsonResponse({'status': 403, 'message': 'Not Allowed'}, status=403)
    try:
        request_body = json.loads(request.body)
        choice = request_body.get('choice')
        feed = request_body.get('feed')
        poll = request_body.get('poll')
        feed_obj = Feed.objects.get(pk=int(feed))
        selected_choice = Choice.objects.get(pk=int(choice), poll__id=int(poll))
        Vote.objects.create(choice=selected_choice, user=request.user)
        selected_choice.votes += 1
        selected_choice.save()
        data = {'post': feed_obj, 'user': request.user}
        page = render_to_string('feed/partials/poll_result.html', data)
        return JsonResponse({'status': 200, 'message': 'Your vote has been submitted!', 'response': page})
    except (ValueError, KeyError):
        return JsonResponse({'status': 422, 'message': 'An error occurred!'}, status=422)

@login_required
def post(request):
    if request.method != 'POST':
        return JsonResponse({'status': 403, 'message': 'Not Allowed'}, status=403)
    form = PostForm(request.POST)
    choice_formset = forms.formset_factory(ChoiceForm, extra=4, can_delete=True)(request.POST, prefix='form')
    images = request.FILES.getlist('image')
    action = request.POST.get('action', 0)
    has_poll = request.POST.get('poll', 0)
    if not form.is_valid():
        return JsonResponse({'status': 403, 'message': form.errors}, status=403)
    text = form.cleaned_data['text']
    feed = Feed.objects.create(user=request.user, text=text)
    for image in images:
      FeedMedia.objects.create(feed=feed, image=image)
    if choice_formset.is_valid() and has_poll == 1:
        feed_poll = Poll.objects.create(feed=feed)
        for choice_form in choice_formset:
            choice_text = choice_form.cleaned_data.get('choice_text')
            if choice_text:
              Choice.objects.create(poll=feed_poll, choice_text=choice_text)
    else:
        for choice_form in choice_formset:
            if choice_form.has_error('choice_text'):
                return JsonResponse({'status': 403, 'message': choice_form.errors}, status=403)
    if int(action) == 1:
        return JsonResponse({'status': 200, 'message': 'Your feed has been posted.'})
    else:
        return render(request, 'feed/partials/feed.html', {'post': feed})

@login_required
def update(request):
  if request.method == 'PATCH':
    request_body = json.loads(request.body)
    content = request_body.get('content')
    feed_id = request_body.get('id')
    instance = Feed.objects.filter(pk=feed_id).update(text=content)
    if instance == 1:
      feed_object = Feed.objects.get(pk=feed_id)
      page = render_to_string('feed/partials/feed.html', {'post': feed_object})
      return JsonResponse({'status': 200, 'feed': page, 'message': 'Your feed has been updated!'})
  return JsonResponse({'status': 403}, status=403)

@login_required
def delete(request, target):
    if request.method != "DELETE":
        return JsonResponse({'status': 404}, status=404)
    feed_id = target
    try:
        feed = Feed.objects.get(pk=feed_id)
        feed.delete()
        return JsonResponse({'status': 200, 'message': 'Deleted!'})
    except Feed.DoesNotExist:
        return JsonResponse({'status': 404}, status=404)

@login_required
def like(request):
    if request.method != "POST":
      return JsonResponse({'status': 403}, status=403)
    try:
        request_body = json.loads(request.body)
        target = request_body.get('target', '')
        if not target:
          return JsonResponse({'status': 403}, status=403)
        feed_object = Feed.objects.get(pk=int(target))
        user = request.user
        is_liked = feed_object.likes.filter(id=user.id).exists()
        if not is_liked:
            feed_object.likes.add(user)
        else:
            feed_object.likes.remove(user)
        feed_type = request.POST.get('type', 0)
        if int(feed_type) == 1:
            template = 'profile/partials/feed.html'
        else:
          template = 'feed/partials/feed.html'
        page = render_to_string(template, context={'post': feed_object})
        return JsonResponse({'status': 200, 'feed': page})
    except Feed.DoesNotExist:
      return JsonResponse({'status': 404}, status=404)

@login_required
def repost(request):
  if request.method != "POST":
    return JsonResponse({'status': 403}, status=403)
  try:
    request_body = json.loads(request.body)
    target = request_body.get('target', '')
    user = request.user
    feed_object = Feed.objects.get(pk=target)
    is_reposted = feed_object.repost.filter(by=user)
    if is_reposted.exists():
      Repost.objects.filter(feed=feed_object, by=request.user).delete()
      feed_object.save()
      return JsonResponse({'status': 201})
    else:
      Repost.objects.create(feed=feed_object, by=request.user)
      feed_object.save()
      page =  render_to_string('feed/partials/repost.html', {'post': feed_object})
      return JsonResponse({'status': 200, 'message': 'Reposted!', 'feed': page})
  except Feed.DoesNotExist:
    return JsonResponse({'status': 404}, status=404)

@login_required
def menu(request, pk):
  try:
    feed_object = Feed.objects.get(pk=pk)
    user_followers = feed_object.user.user_followers()
    return render(request, 'feed/modals/view/menu.html', {'post': feed_object, 'followers': user_followers})
  except Feed.DoesNotExist:
    return JsonResponse({'status': 404}, status = 404)

@login_required
def more(request):
  pass

@login_required
def get_comments(request, feed_id):
    post_object = get_object_or_404(Feed, id=feed_id)
    comment_object = post_object.comments.all()
    if comment_object:
        page = render_to_string('feed/partials/comment.html', {'post': post_object, 'comment': comment_object})
        return JsonResponse({'status': 200, 'comment': page})
    return JsonResponse({'status': 403}, status=404)

@login_required
def post_comment(request):
    if request.method != 'POST':
        return JsonResponse({'status': 403, 'message': 'Not Allowed'}, status=403)
    user = request.user
    feed_id = request.POST['target']
    text = request.POST['comment']
    try:
        post_object = Feed.objects.get(pk=feed_id)
        comment_obj = Comments.objects.create(
            user=user, text=text, feed_id=feed_id)
        if request.FILES:
            images = request.FILES.getlist('comment-image')
            for img in images:
                CommentMedia.objects.create(
                  comment=comment_obj, feed=post_object, image=img)
        data = {'post': post_object, 'comment': comment_obj}
        comment_view = render_to_string('feed/partials/comment.html', data)
        return JsonResponse({'status': 200, 'comment': comment_view})
    except (ValueError, KeyError, Feed.DoesNotExist):
        return JsonResponse({'status': 422, 'message': 'An error occurred'}, status=422)

@login_required
def search(request):
  if request.method == 'POST':
    username = request.POST['username']
    username_object = User.objects.filter(username__icontains = username)
    return render(request, 'search/results.html', {'user_profile_list': username_object})
  else:
    return render(request, 'search/content.html')