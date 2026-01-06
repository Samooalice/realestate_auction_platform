from django.contrib import admin
from .models import CompanyInfo, History, Expert, Achievement, OfficeLocation


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['ceo_name', 'vision']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'title']
    list_filter = ['year']
    ordering = ['-year', '-month']


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'specialty', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'specialty']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'unit', 'order']
    list_editable = ['order']


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'is_main']
    list_filter = ['is_main']
