from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post

# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/index.html'
    paginate_by = 3

def post_list(request):
    # posts = Post.published.all()
    # return render(request, 'blog/post/index.html',
    #    {'posts': posts})
    object_list = Post.published.all()
    paginator = Paginator(object_list, 10) # Trzy posty na każdej stronie
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Jeżeli zmienna page nie jest liczbą całkowitą,
        # wówczas pobierana jest pierwsza strona wyników.
        posts = paginator.page(1)
    except EmptyPage:
        # Jeżeli zmienna page ma wartość większą niż numer ostatniej strony
        # wyników, wtedy pobierana jest ostatnia strona wyników.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/index.html', {
        'page': page,
        'posts': posts})

def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    return render(request, 'blog/post/single.html', {'post': post})
