from django.urls import path
from .feeds import LatestPostsFeed
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('<slug:page>/', views.page_detail, name='page_detail'),
    path('<slug:post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
