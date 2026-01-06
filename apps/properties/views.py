from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import PropertyCategory, Property, PropertyBookmark


def property_list(request):
    """물건 목록"""
    properties = Property.objects.filter(is_published=True)

    # 필터링
    category = request.GET.get('category')
    property_type = request.GET.get('type')
    region = request.GET.get('region')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')

    if category:
        properties = properties.filter(category__slug=category)
    if property_type:
        properties = properties.filter(property_type=property_type)
    if region:
        properties = properties.filter(Q(address__icontains=region) | Q(region__icontains=region))
    if min_price:
        properties = properties.filter(minimum_price__gte=int(min_price))
    if max_price:
        properties = properties.filter(minimum_price__lte=int(max_price))
    if search:
        properties = properties.filter(
            Q(title__icontains=search) |
            Q(address__icontains=search) |
            Q(case_number__icontains=search)
        )

    # 정렬
    sort = request.GET.get('sort', '-auction_date')
    properties = properties.order_by(sort)

    # 페이지네이션
    paginator = Paginator(properties, 12)
    page = request.GET.get('page', 1)
    properties = paginator.get_page(page)

    context = {
        'properties': properties,
        'categories': PropertyCategory.objects.all(),
        'property_types': Property.PROPERTY_TYPE_CHOICES,
    }
    return render(request, 'properties/list.html', context)


def property_detail(request, pk):
    """물건 상세"""
    property_obj = get_object_or_404(Property, pk=pk, is_published=True)
    property_obj.view_count += 1
    property_obj.save(update_fields=['view_count'])

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = PropertyBookmark.objects.filter(
            user=request.user, property=property_obj
        ).exists()

    related_properties = Property.objects.filter(
        category=property_obj.category,
        is_published=True
    ).exclude(pk=pk)[:4]

    context = {
        'property': property_obj,
        'images': property_obj.images.all(),
        'is_bookmarked': is_bookmarked,
        'related_properties': related_properties,
    }
    return render(request, 'properties/detail.html', context)


def property_by_category(request, slug):
    """카테고리별 물건"""
    category = get_object_or_404(PropertyCategory, slug=slug)
    properties = Property.objects.filter(category=category, is_published=True)

    paginator = Paginator(properties, 12)
    page = request.GET.get('page', 1)
    properties = paginator.get_page(page)

    context = {
        'category': category,
        'properties': properties,
    }
    return render(request, 'properties/by_category.html', context)


@login_required
def toggle_bookmark(request, pk):
    """북마크 토글"""
    property_obj = get_object_or_404(Property, pk=pk)
    bookmark, created = PropertyBookmark.objects.get_or_create(
        user=request.user, property=property_obj
    )

    if not created:
        bookmark.delete()
        is_bookmarked = False
    else:
        is_bookmarked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_bookmarked': is_bookmarked})

    return redirect('properties:detail', pk=pk)


@login_required
def bookmark_list(request):
    """북마크 목록"""
    bookmarks = PropertyBookmark.objects.filter(user=request.user).select_related('property')

    paginator = Paginator(bookmarks, 12)
    page = request.GET.get('page', 1)
    bookmarks = paginator.get_page(page)

    context = {
        'bookmarks': bookmarks,
    }
    return render(request, 'properties/bookmarks.html', context)
