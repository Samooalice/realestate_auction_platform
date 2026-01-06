from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import PostCategory, Post, GlossaryTerm, Notice


def post_list(request):
    """게시물 목록"""
    posts = Post.objects.filter(is_published=True)

    # 태그 필터링
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__icontains=tag)

    # 검색
    search = request.GET.get('search')
    if search:
        posts = posts.filter(title__icontains=search) | posts.filter(content__icontains=search)

    # 페이지네이션
    paginator = Paginator(posts, 9)
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'categories': PostCategory.objects.all(),
        'featured_posts': Post.objects.filter(is_published=True, is_featured=True)[:3],
    }
    return render(request, 'info_center/list.html', context)


def post_detail(request, slug):
    """게시물 상세"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    post.view_count += 1
    post.save(update_fields=['view_count'])

    related_posts = Post.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(pk=post.pk)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'info_center/detail.html', context)


def post_by_category(request, slug):
    """카테고리별 게시물"""
    category = get_object_or_404(PostCategory, slug=slug)
    posts = Post.objects.filter(category=category, is_published=True)

    paginator = Paginator(posts, 9)
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'info_center/by_category.html', context)


def glossary(request):
    """용어사전"""
    terms = GlossaryTerm.objects.all()

    # 카테고리 필터링
    category = request.GET.get('category')
    if category:
        terms = terms.filter(category=category)

    # 검색
    search = request.GET.get('search')
    if search:
        terms = terms.filter(term__icontains=search) | terms.filter(definition__icontains=search)

    context = {
        'terms': terms,
        'categories': GlossaryTerm.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'info_center/glossary.html', context)


def notice_list(request):
    """공지사항 목록"""
    notices = Notice.objects.filter(is_published=True)

    # 유형 필터링
    notice_type = request.GET.get('type')
    if notice_type:
        notices = notices.filter(notice_type=notice_type)

    paginator = Paginator(notices, 10)
    page = request.GET.get('page', 1)
    notices = paginator.get_page(page)

    context = {
        'notices': notices,
        'notice_types': Notice.NOTICE_TYPE_CHOICES,
    }
    return render(request, 'info_center/notices.html', context)


def notice_detail(request, pk):
    """공지사항 상세"""
    notice = get_object_or_404(Notice, pk=pk, is_published=True)
    notice.view_count += 1
    notice.save(update_fields=['view_count'])

    prev_notice = Notice.objects.filter(
        is_published=True, pk__lt=pk
    ).order_by('-pk').first()
    next_notice = Notice.objects.filter(
        is_published=True, pk__gt=pk
    ).order_by('pk').first()

    context = {
        'notice': notice,
        'prev_notice': prev_notice,
        'next_notice': next_notice,
    }
    return render(request, 'info_center/notice_detail.html', context)
