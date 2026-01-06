from django.contrib import admin
from .models import SuccessCase, CustomerReview


@admin.register(SuccessCase)
class SuccessCaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'property_type', 'winning_price', 'is_published', 'is_featured', 'view_count']
    list_filter = ['category', 'is_published', 'is_featured']
    list_editable = ['is_published', 'is_featured']
    search_fields = ['title', 'location']


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'category', 'rating', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['category', 'rating', 'is_approved', 'is_featured']
    list_editable = ['is_approved', 'is_featured']
    search_fields = ['author_name', 'content']
