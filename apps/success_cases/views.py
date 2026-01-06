from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import SuccessCase, CustomerReview
from apps.services.models import ServiceCategory


def case_list(request):
    """성공사례 목록"""
    cases = SuccessCase.objects.filter(is_published=True)

    # 필터링
    category = request.GET.get('category')
    if category:
        cases = cases.filter(category__slug=category)

    # 페이지네이션
    paginator = Paginator(cases, 9)
    page = request.GET.get('page', 1)
    cases = paginator.get_page(page)

    context = {
        'cases': cases,
        'categories': ServiceCategory.objects.filter(is_active=True),
    }
    return render(request, 'success_cases/list.html', context)


def case_detail(request, pk):
    """성공사례 상세"""
    case = get_object_or_404(SuccessCase, pk=pk, is_published=True)
    case.view_count += 1
    case.save(update_fields=['view_count'])

    related_cases = SuccessCase.objects.filter(
        category=case.category,
        is_published=True
    ).exclude(pk=pk)[:3]

    context = {
        'case': case,
        'related_cases': related_cases,
    }
    return render(request, 'success_cases/detail.html', context)


def review_list(request):
    """고객 후기 목록"""
    reviews = CustomerReview.objects.filter(is_approved=True)

    # 필터링
    category = request.GET.get('category')
    if category:
        reviews = reviews.filter(category__slug=category)

    # 페이지네이션
    paginator = Paginator(reviews, 12)
    page = request.GET.get('page', 1)
    reviews = paginator.get_page(page)

    context = {
        'reviews': reviews,
        'categories': ServiceCategory.objects.filter(is_active=True),
    }
    return render(request, 'success_cases/reviews.html', context)
