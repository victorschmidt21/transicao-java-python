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


def send_budget_email(budget, request):
    """
    Envia e-mail ao cliente com os dados do orçamento criado.
    
    Args:
        budget: Instância do modelo Budget
        request: Objeto request para adicionar mensagens de feedback
    """
    try:
        if budget.customer.email:
            context = {'budget': budget}
            html_content = render_to_string('emails/budget_email.html', context)
            text_content = render_to_string('emails/budget_email.txt', context)
            
            subject = f'Orçamento #{budget.id} - GestãoApp'
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@gestaoapp.com')
            to_email = [budget.customer.email]
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=to_email
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            logger.info(f'E-mail enviado com sucesso')
            messages.success(
                request,
                f'Orçamento criado e e-mail enviado'
            )
        else:
            messages.warning(
                request,
                f'Cliente não possui e-mail cadastrado.'
            )
    except Exception as e:
        logger.error(
            f'Erro ao enviar e-mail de orçamento #{budget.id}: {str(e)}',
            exc_info=True
        )
        messages.error(
            request,
            f'Orçamento #{budget.id} criado, mas houve um erro ao enviar o e-mail: {str(e)}'
        )


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

        # Envia e-mail ao cliente
        send_budget_email(budget, request)

        return redirect('budget_index')

    return render(request, 'create.html', {
        'products': products,
        'customers': customers,
        'title': 'Novo Orçamento'
    })


def view_delete(request, id):
    budget = get_object_or_404(models.Budget, id=id)
    budget.delete()
    return redirect('budget_index')