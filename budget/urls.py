from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.view_index),
    path('create/', views.view_create),
    path('edit/<int:id>/', views.view_edit, name='edit'),
    path('delete/<int:id>/', views.view_delete, name='delete'),
]
