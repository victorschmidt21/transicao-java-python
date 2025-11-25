from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('edit/<int:id>/', views.customer_edit, name='customer_edit'),
    path('delete/<int:id>/', views.customer_delete, name='customer_delete'),
]
