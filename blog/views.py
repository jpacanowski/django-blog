from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/index.html',
        {'posts': posts})

def post_detail(request, post):
    post = get_object_or_404(Post,
        slug=post, status='published')
    return render(request, 'blog/post/single.html',
        {'post': post})
