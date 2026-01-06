from django.shortcuts import render
from django.db.models import Count
from .models import HeroBanner, SiteStatistics, Partner, FAQ
from apps.services.models import ServiceCategory
from apps.properties.models import Property
from apps.success_cases.models import SuccessCase, CustomerReview
from apps.info_center.models import Post


def home(request):
    """메인 페이지"""
    context = {
        'banners': HeroBanner.objects.filter(is_active=True),
        'statistics': SiteStatistics.objects.first(),
        'services': ServiceCategory.objects.filter(is_active=True)[:5],
        'featured_properties': Property.objects.filter(
            is_recommended=True
        )[:6],
        'success_cases': SuccessCase.objects.filter(
            is_published=True, is_featured=True
        )[:4],
        'reviews': CustomerReview.objects.filter(
            is_approved=True, is_featured=True
        )[:6],
        'partners': Partner.objects.filter(is_active=True),
        'recent_posts': Post.objects.filter(is_published=True)[:4],
    }
    return render(request, 'core/home.html', context)


def faq_list(request):
    """FAQ 페이지"""
    faqs = FAQ.objects.filter(is_active=True)
    categories = faqs.values('category').annotate(count=Count('id'))

    selected_category = request.GET.get('category', '')
    if selected_category:
        faqs = faqs.filter(category=selected_category)

    context = {
        'faqs': faqs,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'core/faq.html', context)
