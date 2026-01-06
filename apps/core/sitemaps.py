from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.services.models import ServiceCategory
from apps.properties.models import Property
from apps.success_cases.models import SuccessCase
from apps.academy.models import Course
from apps.info_center.models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:faq', 'company:about', 'services:list',
                'properties:list', 'success_cases:list', 'academy:list',
                'info_center:list', 'consultation:form']

    def location(self, item):
        return reverse(item)


class ServiceCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ServiceCategory.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class PropertySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return Property.objects.filter(is_recommended=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class SuccessCaseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return SuccessCase.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()


class CourseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Course.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
