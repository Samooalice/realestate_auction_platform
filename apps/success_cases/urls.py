from django.urls import path
from . import views

app_name = 'success_cases'

urlpatterns = [
    path('', views.case_list, name='list'),
    path('<int:pk>/', views.case_detail, name='detail'),
    path('reviews/', views.review_list, name='reviews'),
]
