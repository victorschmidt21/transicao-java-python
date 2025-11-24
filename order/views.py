from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
import logging

from product.models import Product
from customers.models import Customer
import json

logger = logging.getLogger(__name__)

from product.models import Product
from customers.models import Customer
import json
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

def send_order_email(order, request):
    """
    Envia e-mail ao cliente com os dados do pedido criado.
    
    Args:
        order: Instância do modelo Order
        request: Objeto request para adicionar mensagens de feedback
    """
    try:
        if order.customer.email:
            context = {'order': order}
            html_content = render_to_string('emails/order_email.html', context)
            text_content = render_to_string('emails/order_email.txt', context)
            
            subject = f'Pedido #{order.id} - GestãoApp'
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@gestaoapp.com')
            to_email = [order.customer.email]
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=to_email
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            logger.info(f'E-mail de pedido enviado com sucesso')
            messages.success(
                request,
                f'Pedido criado e e-mail enviado'
            )
        else:
            messages.warning(
                request,
                f'Cliente não possui e-mail cadastrado.'
            )
    except Exception as e:
        logger.error(
            f'Erro ao enviar e-mail de pedido #{order.id}: {str(e)}',
            exc_info=True
        )
        messages.error(
            request,
            f'Pedido #{order.id} criado, mas houve um erro ao enviar o e-mail: {str(e)}'
        )

@login_required
def view_index(request):
    search = request.GET.get("search", "").strip()
    orders = models.Order.objects.all()

    if search:
        orders = orders.filter(id =search)

    return render(request, 'order.html', {
        'orders': orders,
        'search': search,
    })

@login_required
def view_create(request):
    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('cliente')
        customer = Customer.objects.get(id=customer_id)

        products_json = request.POST.get('products', '[]')

        products_data = json.loads(products_json)

        if not products_data:
            messages.error(request, 'Nenhum produto selecionado.')
            return render(request, 'create_order.html', {
                'products': products,
                'customers': customers,
                'title': 'Novo pedido'
            })

        for item in products_data:
            product_id = item.get('id')
            quantity = int(item.get('quantity', 1))
            product = Product.objects.get(id=product_id)
            
            if product.qty_stock < quantity:
                messages.error(request, f'Estoque insuficiente para o produto {product.description}. Disponível: {product.qty_stock}')
                return render(request, 'create_order.html', {
                    'products': products,
                    'customers': customers,
                    'title': 'Novo pedido'
                })

        order = models.Order.objects.create(customer=customer, total_amount=0)
        total_amount = Decimal('0.00')

        for item in products_data:
            product_id = item.get('id')
            quantity = int(item.get('quantity', 1))
            product = Product.objects.get(id=product_id)

            # Decrement stock
            product.qty_stock -= quantity
            product.save()

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

        # Envia e-mail ao cliente
        send_order_email(order, request)

        return redirect('/order/')

    return render(request, 'create_order.html', {
        'products': products,
        'customers': customers,
        'title': 'Novo pedido'
    })

@login_required
def view_delete(request, id):
    order = get_object_or_404(models.Order, id=id)
    order.delete()
    return redirect('order_index')