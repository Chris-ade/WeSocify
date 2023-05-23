from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from moments import views

app_name = "moments"

urlpatterns = [
    path('moments', views.MomentView.get, name='moments'),
    path('api/moments/', views.MomentListAPI.as_view()),
    #path('api/moments/post', views.PostFeedAPI.as_view()),
    #path('api/<username>/moments/<int:pk>/', views.GetFeedAPI.as_view()),
    path('moments/<str:switch>/create', views.MomentView.post, name='moments/create'),
    path('moments/create', views.MomentView.post, name='moments/create'),
]