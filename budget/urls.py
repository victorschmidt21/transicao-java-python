from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.view_index, name='budget_index'),
    path('create/', views.view_create),
    path('detail/<int:id>/', views.view_detail, name='budget_detail'),
    path('delete/<int:id>/', views.view_delete, name='delete'),
    path('convert/<int:id>/', views.view_convert_to_order, name='convert_to_order'),
]
