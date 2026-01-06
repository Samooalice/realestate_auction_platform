from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.about, name='about'),
    path('greeting/', views.ceo_greeting, name='ceo_greeting'),
    path('history/', views.history, name='history'),
    path('experts/', views.experts, name='experts'),
    path('location/', views.location, name='location'),
]
