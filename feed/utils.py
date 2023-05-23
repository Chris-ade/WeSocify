from .models import *
from django.db.models import Q
from accounts.models import *
from math import ceil

PER_PAGE = 10

""" Helper functions """
def pagination(request, obj):
    """
    This function takes a request object and a list of items, and returns a
    paginated version of the list of items for the current page.

    Parameters:
        request (HttpRequest): The request object
        obj (List): A list of items to be paginated

    Returns:
        Tuple: A tuple containing the paginated list of items for the current page, the current page number and total number of pages.

    Example:
        result = pagination(request, obj_list)
        feed, page, total_pages = result
    """
    try:
        page = int(request.POST.get('page', 1))
    except ValueError:
        page = 1
    per_page = PER_PAGE
    total_items = len(obj)
    total_pages = ceil(total_items / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    if page > total_pages or page < 1:
        feed = []
    else:
        feed = obj[start:end]
    return feed, page, total_pages

"""
Returns the list of feeds related to the user
"""
def get_user_feed(request, type=None):
    user = request.user
    following_ids = user.following.values_list('id', flat=True)
    feed_objects = Feed.objects.filter(
        Q(user__id__in=following_ids) | Q(user=user)
    ).prefetch_related(
        'images', 'comments', 'comments__comment_image',
        'feed_poll', 'feed_poll__choices', 'feed_poll__choices__poll_votes',
        'repost'
    ).order_by('-id')
    if type == 'queryset':
        return feed_objects
    return list(feed_objects)

"""
Returns the list of user suggestions
"""
def get_user_suggestions(request):
    current_user = request.user
    following_ids = current_user.following.values_list('id', flat=True)
    suggestions = User.objects.exclude(id__in=following_ids).exclude(id=current_user.id)
    suggestions = suggestions.order_by("?")[:10]
    return list(suggestions)