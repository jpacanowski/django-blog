from django.urls import path
from .feeds import LatestPostsFeed
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('<slug:slug>/', views.PagePost_detail, name='PagePost_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
