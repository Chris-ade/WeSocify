from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from feed.utils import *
from .utils import *

class RegisterView(generics.CreateAPIView):
    """
    A class-based view for handling user registration.

    This view handles user registration and is designed to be called by a client-side application. The view
    accepts a request with the necessary data to create a new user, serializes the data using the 
    `RegisterSerializer` class, and returns a response with the serialized data of the newly created user.

    The view does not require authentication or authorization, as indicated by the empty `authentication_classes`
    and `permission_classes` attributes.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    """
    A class-based view for handling user authentication.

    This view is responsible for authenticating a user using the provided username and password. If the provided
    credentials are valid, the view returns a response with the user's authentication token. If the credentials are
    invalid, the view returns a 400 Bad Request response with an error message indicating that the provided
    credentials are incorrect.

    The view does not require authorization, as indicated by the empty `permission_classes` attribute.
    """
    permission_classes = ()
    
class FeedsView(APIView):
    """
    Retrieve all the feeds that are available to the current user.
    
    Args:
    request: The incoming request.

    Returns:
    JsonResponse: A JSON representation of the feed data.
    """
    def get(self, request):
        feed = get_user_feed(request, 'queryset')
        serializer = FeedSerializer(feed, many=True)
        return response(serializer.data)

    def post(self, request):
        """
        Handles a POST request for user authentication.

        This method extracts the user's username and password from the request data, and uses the
        `django.contrib.auth.authenticate` function to authenticate the user. If the user is successfully
        authenticated, the method returns a response with the user's authentication token. If the user is not
        successfully authenticated, the method returns a 400 Bad Request response with an error message indicating
        that the provided credentials are incorrect.
        """
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return response({"token": user.auth_token.key})
        else:
            return abort(400, "Incorrect credentials")

class FeedView(APIView):
    """
    A class-based view for handling feed CRUD operations.

    This view is responsible for handling Create, Read, Update, and Delete (CRUD) operations on feed objects. The view
    supports retrieving a feed by its primary key (pk) and username, updating a feed, and deleting a feed. If the
    requested feed does not exist, the view returns a 404 Not Found response. If a user attempts to perform an
    unauthorized operation, such as deleting a feed that they do not own, the view returns a 403 Forbidden response.

    The view assumes that the client provides the feed's pk and username in the URL, as well as any necessary data for
    update operations in the request body.
    """

    def get(self, request, username, pk):
        """
        Handles a GET request for a single feed.

        This method retrieves the requested feed by its primary key (pk) and username, and returns a response with the
        feed data. If the requested feed does not exist, the method returns a 404 Not Found response.
        """
        try:
            feed = Feed.objects.get(pk=pk, user__username=username)
            serializer = FeedSerializer(feed)
            return response(serializer.data)
        except Feed.DoesNotExist:
            return abort(404)

    def put(self, request, username, pk):
        """
        Handles a PUT request for a single feed.

        This method retrieves the requested feed by its primary key (pk) and username, updates the feed with the data
        provided in the request body, and returns a response with the updated feed data. If the requested feed does not
        exist, the method returns a 404 Not Found response. If the provided data is invalid, the method returns a 400
        Bad Request response with an error message.
        """
        try:
            feed = Feed.objects.get(pk=pk, user__username=username)
            data = JSONParser().parse(request)
            serializer = FeedSerializer(feed, data=data)
            if serializer.is_valid():
                serializer.save()
                return response(serializer.data)
            return abort(400, serializer.errors)
        except Feed.DoesNotExist:
            return abort(404)

    def delete(self, request, username, pk):
        """
        Handles a DELETE request for a single feed.

        This method retrieves the requested feed by its primary key (pk) and username, and deletes the feed. If the
        requested feed does not exist, the method returns a 404 Not Found response. If the request user is not the owner
        of the feed, the method returns a 403 Forbidden response. If the feed is successfully deleted, the method
        returns a 204 No Content response with a success message.
        """
        try:
            feed = Feed.objects.get(pk=pk, user__username=username)
            if not request.user == feed.user:
                return abort(403)
            else:
                feed.delete()
                return response({"message": "Successfully deleted feed."}, 204)
        except Feed.DoesNotExist:
            return abort(404)

def get_feed_likes(request, username, pk):
    try:
        feed = Feed.objects.get(pk=pk, user__username=username)
        likes = feed.likes.all()
        serializer = LikesSerializer(likes, many=True)
        usernames = [item['username'] for item in serializer.data]
        return response([usernames])
    except Feed.DoesNotExist:
        return abort(404)

class ProfileView(APIView):
    def get(self, request, username):
        try:
          obj = User.objects.get(username=username)
          serializer = UserSerializer(obj)
          return response(serializer.data)
        except User.DoesNotExist:
          return abort(404)

def get_profile_media(request, username):
    try:
      user_obj = User.objects.get(username=username)
      feeds = Feed.objects.filter(user__username=username, images__isnull=False).prefetch_related('images').order_by('-created_at').exists()
      if feeds:
        serializer = FeedSerializer(feeds, many=True)
        return response(serializer.data)
      return HttpResponse(status=204)
    except User.DoesNotExist:
      return abort(404)

def get_profile_replies(request, username):
    try:
        user_obj = User.objects.get(username=username)
        feeds = Feed.objects.filter(user__username=username, comments__user__username=username).distinct().order_by('-created_at').exists()
        if feeds:
            serializer = FeedSerializer(feeds, many=True)
            return response(serializer.data)
        return HttpResponse(status=204)
    except User.DoesNotExist:
        return abort(404)

def get_profile_likes(request, username):
    """
    Endpoint for retreiving all the feeds that an account has liked.

    Parameters:
        request (HttpRequest): The incoming request object.
        username (str): The username of the account whose liked feeds are to be displayed.

    Returns:
        JsonResponse: A JSON representation of the feeds.

    Example:
        GET /{username}/likes/
    """
    try:
        user_obj = User.objects.get(username=username)
        feeds = Feed.objects.filter(likes__username=username).order_by('-created_at').exists()
        if feeds:
            serializer = FeedSerializer(feeds, many=True)
            return response(serializer.data)
        return response({'status': 204, 'message': f'@{user_obj.username} hasn\'t posted media.'}, 204)
    except User.DoesNotExist:
        return abort(404)

class FollowView(APIView):
    """
      Follow or unfollow a user
      Args:
          request: The request object
          user: The username of the user to follow or unfollow
      Returns:
          redirect: Redirects the user to the profile page of the user they are following or unfollowing
    """
    def post(self, request, username):
        try:
          user = User.objects.get(username=username)
          current_user = request.user
          following = user.followers.all()
          if not user.username == current_user.username:
              if current_user in following:
                  user.followers.remove(current_user.id)
              else:
                  user.followers.add(current_user.id)
              followers = FollowersSerializer(user)
              return response(followers.data)
          return abort(403)
        except User.DoesNotExist:
          return abort(400)

def get_followers(request, username):
    try:
        user_object = User.objects.get(username=username)
        followers = FollowersSerializer(user_object)
        return response(followers.data)
    except User.DoesNotExist:
        return abort(404)

def get_following(request, username):
    try:
        user_object = User.objects.get(username=username)
        following = FollowingSerializer(user_object)
        return response(following.data)
    except User.DoesNotExist:
        return abort(404)

class SettingsView(APIView):
    """
    A class-based view for handling the settings of a user.

    The view supports the following actions:
    - retrieve the current settings of a user (GET request)
    - update the settings of a user (POST request)
    """

    def get(self, request):
        """
        Retrieve the current settings of a user.

        Parameters:
        - request (django.http.request.HttpRequest): the HTTP request object

        Returns:
        - django.http.response.Response: a response containing the serialized user data

        Raises:
        - None
        """
        user = request.user
        serializer = SettingsSerializer(user)
        return response(serializer.data)

    def patch(self, request):
        """
        Update the settings of a user.

        Parameters:
        - request (django.http.request.HttpRequest): the HTTP request object

        Returns:
          A response containing the updated serialized user data

        Raises:
        - django.http.response.HttpResponseBadRequest: if the request data is not valid
        """
        user = request.user
        serializer = SettingsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data)
        return abort(400, serializer.errors)