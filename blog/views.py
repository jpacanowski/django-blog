from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag
from .forms import CommentForm
from .models import Post, Comment

# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/index.html'
    paginate_by = 3

def post_list(request, tag_slug=None):
    # posts = Post.published.all()
    # return render(request, 'blog/post/index.html',
    #    {'posts': posts})
    object_list = Post.published.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

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
        'posts': posts,
        'tag': tag})

def post_detail(request, post):

    post = get_object_or_404(Post, slug=post, status='published')
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # Komentarz został opublikowany
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Utworzenie obiektu Comment, ale jeszcze nie zapisujemy go w bazie danych
            new_comment = comment_form.save(commit=False)
            # Przypisanie komentarza do bieżącego posta
            new_comment.post = post
            # Zapisanie komentarza w bazie danych
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Lista podobnych postów
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags','-published_at')[:4]

    return render(request, 'blog/post/single.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts})
