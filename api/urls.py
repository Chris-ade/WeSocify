from django.urls import path
from api import views

app_name = "api"

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('feed/', views.FeedsView.as_view()),
    path('settings/', views.SettingsView.as_view()),
    path('<username>/feed/<int:pk>/', views.FeedView.as_view()),
    path('<username>/feed/<int:pk>/likes/', views.get_feed_likes),
    path('<username>/', views.ProfileView.as_view()),
    path('<username>/media/', views.get_profile_media),
    path('<username>/with_replies/', views.get_profile_replies),
    path('<username>/likes/', views.get_profile_likes),
    path('<username>/follow/', views.FollowView.as_view()),
    path('<username>/followers/', views.get_followers),
    path('<username>/following/', views.get_following),
]