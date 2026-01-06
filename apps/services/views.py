from django.shortcuts import render, get_object_or_404
from .models import ServiceCategory, Service, PricingPlan, ProcessStep


def service_list(request):
    """서비스 목록"""
    context = {
        'categories': ServiceCategory.objects.filter(is_active=True),
    }
    return render(request, 'services/list.html', context)


def service_detail(request, slug):
    """서비스 상세"""
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)

    context = {
        'category': category,
        'services': category.services.all(),
        'pricing': category.pricing_plans.all(),
        'process_steps': ProcessStep.objects.all(),
    }
    return render(request, 'services/detail.html', context)


def pricing(request):
    """가격 안내"""
    context = {
        'categories': ServiceCategory.objects.filter(is_active=True),
        'pricing_plans': PricingPlan.objects.all(),
    }
    return render(request, 'services/pricing.html', context)


def process(request):
    """진행 절차"""
    context = {
        'steps': ProcessStep.objects.all(),
    }
    return render(request, 'services/process.html', context)
