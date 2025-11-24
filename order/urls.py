from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_index, name='order_index'),
    path('create/', views.view_create),
    path('delete/<int:id>/', views.view_delete, name='delete'),
]