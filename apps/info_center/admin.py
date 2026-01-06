from django.contrib import admin
from .models import PostCategory, Post, GlossaryTerm, Notice


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author_name', 'is_published', 'is_featured', 'view_count', 'created_at']
    list_filter = ['category', 'is_published', 'is_featured']
    list_editable = ['is_published', 'is_featured']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'category', 'order']
    list_filter = ['category']
    list_editable = ['order']
    search_fields = ['term', 'definition']


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'notice_type', 'is_pinned', 'is_published', 'view_count', 'created_at']
    list_filter = ['notice_type', 'is_pinned', 'is_published']
    list_editable = ['is_pinned', 'is_published']
    search_fields = ['title', 'content']
