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
    orders = models.Order.objects.all()

    if search:
        orders = orders.filter(id =search)

    return render(request, 'order.html', {
        'orders': orders,
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

        order = models.Order.objects.create(customer=customer, total_amount=0)
        total_amount = Decimal('0.00')

        for item in products_data:
            product_id = item.get('id')
            quantity = int(item.get('quantity', 1))
            product = Product.objects.get(id=product_id)

            price_unit = product.price
            price_total = price_unit * quantity

            models.OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                subtotal=price_total,
            )

            total_amount += price_total

        order.total_amount = total_amount
        order.save()

        return redirect('/order/')

    return render(request, 'create_order.html', {
        'products': products,
        'customers': customers,
        'title': 'Novo pedido'
    })


def view_delete(request, id):
    order = get_object_or_404(models.Order, id=id)
    order.delete()
    return redirect('order_index')