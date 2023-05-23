from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from rest_framework.authtoken.models import Token
from feed.models import *

class FeedMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedMedia
        fields = ['image',]

class CommentsMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMedia
        fields = ['image',]

class CommentSerializer(serializers.ModelSerializer):
    comment_image = CommentsMediaSerializer(many=True)

    class Meta:
        model = Comments
        fields = "__all__"

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user', 'choice']

class ChoiceSerializer(serializers.ModelSerializer):
    poll_votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'poll', 'choice_text', 'poll_votes']

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'feed', 'pub_date', 'choices']

class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repost
        fields = ['id', 'by', 'feed']

class FeedSerializer(serializers.ModelSerializer):
    images = FeedMediaSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    feed_poll = PollSerializer(many=True, read_only=True)
    repost = RepostSerializer(many=True, read_only=True)
    likes = StringRelatedField(many=True)

    class Meta:
        model = Feed
        fields = ['id', 'user', 'text', 'likes', 'images', 'comments', 'feed_poll', 'repost']

class UserSerializer(serializers.ModelSerializer):
    followers = StringRelatedField(many=True)
    following = StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'bio', 'avatar', 'cover', 'location', 'website', 'followers', 'following']
        extra_kwargs = {'password': {'write_only': True}}

class FollowersSerializer(serializers.ModelSerializer):
    followers = StringRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ['followers']

class FollowingSerializer(serializers.ModelSerializer):
    following = StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['following']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}, 'birth_date': {'write_only': True}}

    def create(self, validated_data):
        user = User(
          email=validated_data['email'],
          username=validated_data['username'],
          name=validated_data['name'],
          birth_date=validated_data['birth_date']
          )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class SettingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    
    class Meta:
        model = User
        fields = ['name', 'bio', 'location', 'website', 'birth_date']

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']