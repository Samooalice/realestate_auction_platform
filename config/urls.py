"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from apps.core.sitemaps import (
    StaticViewSitemap, ServiceCategorySitemap, PropertySitemap,
    SuccessCaseSitemap, CourseSitemap, PostSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'services': ServiceCategorySitemap,
    'properties': PropertySitemap,
    'success_cases': SuccessCaseSitemap,
    'courses': CourseSitemap,
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('company/', include('apps.company.urls')),
    path('services/', include('apps.services.urls')),
    path('properties/', include('apps.properties.urls')),
    path('success-cases/', include('apps.success_cases.urls')),
    path('academy/', include('apps.academy.urls')),
    path('info/', include('apps.info_center.urls')),
    path('consultation/', include('apps.consultation.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
