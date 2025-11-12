from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models

from product.models import Product
from customers.models import Customer
import json


# Create your views here.

def view_index(request):
    budgets = models.Budget.objects.all()
    return render(request, 'index.html', {'budgets': budgets})

def view_create(request):
    if request.method == 'POST':
        customer_id = request.POST.get('cliente')
        products_json = request.POST.get('products')  # vem como string JSON

        try:
            products = json.loads(products_json) if products_json else []
        except json.JSONDecodeError:
            products = []

        # Exemplo: processar os produtos
        for p in products:
            print(f"Produto: {p['name']} | Qtd: {p['quantity']} | Total: {p['total_value']}")

        # Aqui você pode salvar no banco normalmente
        # ...

        return HttpResponse("Venda cadastrada com sucesso!")
    
    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'create.html', { 'products': products, 'customers': customers })

def view_edit(request, id):
    return render(request, 'budget/edit.html', {'id': id})

def view_delete(request, id):
    return render(request, 'budget/delete.html', {'id': id})