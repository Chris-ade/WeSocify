class FeedList(generics.ListAPIView):
    queryset = user_feed.objects.all()
    serializer_class = UserFeedSerializer

class GetFeed(generics.RetrieveAPIView):
    queryset = user_feed.objects.all()
    serializer_class = UserFeedSerializer
    
class PostFeed(generics.CreateAPIView):
    queryset = user_feed.objects.all()
    serializer_class = UserFeedSerializer
