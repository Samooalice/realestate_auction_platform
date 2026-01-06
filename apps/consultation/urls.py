from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('', views.consultation_form, name='form'),
    path('complete/', views.consultation_complete, name='complete'),
]
