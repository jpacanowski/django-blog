from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag
from .forms import CommentForm, SearchForm
from .models import Page, Post, Comment

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

def PagePost_detail(request, slug):

    # page = Page.objects.get(slug=post)
    # if Page.objects.get(slug=post).exists():
    #     page = Page.objects.get(slug=post)
    #     pages = Page.published.values('title')
    #     return render(request, 'blog/page/single.html', {
    #         'page': page,
    #         'pages': pages})

    try:
        page = Page.published.get(slug=slug)
        pages = Page.published.all()
        return render(request, 'blog/page/single.html', {
            'page': page,
            'pages': pages})

    except Page.DoesNotExist:
        post = get_object_or_404(Post, slug=slug, status='published')
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

        # Lista ostatnio opublikowanych postów
        latest_posts = Post.published.order_by('-published_at')[:5]

        # Lista postów w sidebar
        pages = Page.published.all()

        return render(request, 'blog/post/single.html', {
            'post': post,
            'pages': pages,
            'comments': comments,
            'comment_form': comment_form,
            'similar_posts': similar_posts,
            'latest_posts': latest_posts})

# def page_detail(request, page):

#     page = get_object_or_404(Page, slug=page, status='published')
#     pages = Page.published.values('title')

#     return render(request, 'blog/page/single.html', {
#         'page': page,
#         'pages': pages})

def post_search(request):

    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:

        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']

            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

    return render(request, 'blog/post/search.html', {
        'form': form,
        'query': query,
        'results': results})
