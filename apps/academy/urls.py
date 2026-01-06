from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/enroll/', views.enroll, name='enroll'),
    path('instructors/', views.instructor_list, name='instructors'),
    path('free-lectures/', views.free_lecture_list, name='free_lectures'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
