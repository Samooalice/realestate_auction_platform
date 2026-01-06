from django.contrib import admin
from .models import PropertyCategory, Property, PropertyImage, PropertyBookmark


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'court', 'auction_date', 'minimum_price', 'is_recommended', 'is_weekly_pick']
    list_filter = ['property_type', 'court', 'risk_level', 'is_recommended', 'is_weekly_pick', 'auction_status']
    list_editable = ['is_recommended', 'is_weekly_pick']
    search_fields = ['title', 'case_number', 'address']
    date_hierarchy = 'auction_date'
    inlines = [PropertyImageInline]


@admin.register(PropertyBookmark)
class PropertyBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'property__title']
