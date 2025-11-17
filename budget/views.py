from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from decimal import Decimal
from django.shortcuts import get_object_or_404

from product.models import Product
from customers.models import Customer
import json

def view_index(request):
    search = request.GET.get("search", "").strip()
    budgets = models.Budget.objects.all()

    if search:
        budgets = budgets.filter(id =search)

    return render(request, 'index.html', {
        'budgets': budgets,
        'search': search,
    })

def view_create(request):
    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('cliente')
        customer = Customer.objects.get(id=customer_id)

        products_json = request.POST.get('products', '[]')
        products_data = json.loads(products_json)

        budget = models.Budget.objects.create(customer=customer, total_amount=0)
        total_amount = Decimal('0.00')

        for item in products_data:
            product_id = item.get('id')
            quantity = int(item.get('quantity', 1))
            product = Product.objects.get(id=product_id)

            price_unit = product.price
            price_total = price_unit * quantity

            models.BudgetItem.objects.create(
                budget=budget,
                product=product,
                quantity=quantity,
                subtotal=price_total,
            )

            total_amount += price_total

        budget.total_amount = total_amount
        budget.save()

        return redirect('/budget/')

    return render(request, 'create.html', {
        'products': products,
        'customers': customers,
        'title': 'Novo Orçamento'
    })


def view_delete(request, id):
    budget = get_object_or_404(models.Budget, id=id)
    budget.delete()
    return redirect('budget_index')