from django.urls import path
from . import views

app_name = 'info_center'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.post_by_category, name='by_category'),
    path('glossary/', views.glossary, name='glossary'),
    path('notice/', views.notice_list, name='notices'),
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
]
