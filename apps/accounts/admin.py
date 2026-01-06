from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'user_type', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'phone']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('phone', 'user_type', 'marketing_agreed')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('추가 정보', {'fields': ('phone', 'user_type', 'marketing_agreed')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_region', 'budget_range', 'interest_type']
    list_filter = ['budget_range', 'interest_type']
    search_fields = ['user__username', 'preferred_region']
