from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service_type', 'status', 'assigned_to', 'created_at']
    list_filter = ['service_type', 'status', 'budget_range', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'phone', 'email', 'preferred_region']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('신청자 정보', {
            'fields': ('name', 'phone', 'email')
        }),
        ('상담 내용', {
            'fields': ('service_type', 'budget_range', 'preferred_region', 'message')
        }),
        ('동의 사항', {
            'fields': ('privacy_agreed', 'marketing_agreed')
        }),
        ('처리 정보', {
            'fields': ('status', 'assigned_to', 'admin_memo', 'contacted_at')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
