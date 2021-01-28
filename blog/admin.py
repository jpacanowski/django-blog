from django.contrib import admin
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'published_at', 'status')
    list_filter = ('status', 'created_at', 'published_at', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('status', '-published_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'body')
