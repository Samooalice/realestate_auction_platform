from django.shortcuts import render
from .models import CompanyInfo, History, Expert, Achievement, OfficeLocation


def about(request):
    """회사 소개"""
    context = {
        'company': CompanyInfo.objects.first(),
        'achievements': Achievement.objects.all(),
        'experts': Expert.objects.filter(is_active=True)[:4],
    }
    return render(request, 'company/about.html', context)


def ceo_greeting(request):
    """대표 인사말"""
    context = {
        'company': CompanyInfo.objects.first(),
    }
    return render(request, 'company/ceo_greeting.html', context)


def history(request):
    """회사 연혁"""
    histories = History.objects.all()
    years = histories.values_list('year', flat=True).distinct()

    context = {
        'histories': histories,
        'years': years,
    }
    return render(request, 'company/history.html', context)


def experts(request):
    """전문가 소개"""
    context = {
        'experts': Expert.objects.filter(is_active=True),
    }
    return render(request, 'company/experts.html', context)


def location(request):
    """오시는 길"""
    context = {
        'locations': OfficeLocation.objects.all(),
        'main_office': OfficeLocation.objects.filter(is_main=True).first(),
    }
    return render(request, 'company/location.html', context)
