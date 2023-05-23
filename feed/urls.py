from django.urls import path
from feed import views

app_name = "feed"

urlpatterns = [
    path('home', views.home, name='home'),
    path('explore', views.home, name='explore'),
    path('notifications', views.home, name='notifications'),
    path('messages', views.home, name='messages'),
    path('questions', views.home, name='questions'),
    path('rooms', views.home, name='rooms'),
    path('feed/compose/', views.compose, name='compose'),
    path('feed/post/', views.post, name='post'),
    path('search', views.home, name='search'),
    path('<username>/feed/<int:pk>/', views.view, name='view'),
    path('feed/like/', views.like, name='like'),
    path('feed/poll/vote/', views.vote, name='vote'),
    path('feed/menu/<int:pk>/', views.menu, name='menu'),
    path('feed/edit/', views.update, name='edit'),
    path('feed/delete/<int:target>/', views.delete, name='delete'),
    path('feed/more/', views.more, name='more'),
    path('feed/comment/', views.post_comment, name='comment'),
    path('feed/repost/', views.repost, name='repost'),
]