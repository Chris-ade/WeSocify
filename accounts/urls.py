from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('welcome', views.welcome, name='welcome'),
    path('register', views.register, name='register'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy_policy, name='privacy'),
    path('logout', views.logout, name='logout'),
    path('<username>', views.get, name='profile'),
    path('<username>/feeds/', views.feeds, name='feeds'),
    path('<username>/with_replies/', views.with_replies, name='with_replies'),
    path('<username>/media/', views.media, name='media'),
   path('<username>/likes/', views.likes, name='likes'),
    path('<username>/followers/', views.followers, name='followers'),
    path('<username>/following/', views.following, name='following'),
    path('accounts/follow/<str:user>/', views.follow, name='follow'),
    path('accounts/settings/', views.settings, name='settings'),
]