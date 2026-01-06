from django.contrib import admin
from .models import CourseCategory, Course, Instructor, Enrollment, FreeLecture, CourseReview


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'start_date', 'price', 'current_students', 'max_students', 'is_active', 'is_enrolling']
    list_filter = ['category', 'is_active', 'is_enrolling']
    list_editable = ['is_active', 'is_enrolling']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_date'


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'name', 'payment_status', 'payment_amount', 'created_at']
    list_filter = ['course', 'payment_status', 'payment_method']
    search_fields = ['user__username', 'name', 'phone', 'email']
    date_hierarchy = 'created_at'


@admin.register(FreeLecture)
class FreeLectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'view_count', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved']
    list_editable = ['is_approved']
