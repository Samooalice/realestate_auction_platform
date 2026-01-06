from django.contrib import admin
from .models import ServiceCategory, Service, PricingPlan, ProcessStep


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['category', 'overview']
    search_fields = ['overview', 'target_customers']


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_type', 'price_display', 'is_popular', 'order']
    list_filter = ['price_type', 'is_popular']
    list_editable = ['is_popular', 'order']


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ['title', 'step_number']
    list_editable = ['step_number']
    ordering = ['step_number']
