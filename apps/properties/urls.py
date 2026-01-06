from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('<int:pk>/', views.property_detail, name='detail'),
    path('category/<slug:slug>/', views.property_by_category, name='by_category'),
    path('bookmark/<int:pk>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmark_list, name='bookmarks'),
]
