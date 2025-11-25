from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Product
from .forms import ProductForm


def product_list(request):
    """Lista todos os produtos"""
    try:
        products = Product.objects.select_related('supplier').all()

        search = request.GET.get('search', '')
        if search:
            products = products.filter(description__icontains=search)

        context = {
            'products': products,
            'search': search
        }
        return render(request, 'product/product_list.html', context)

    except Exception:
        messages.error(request, 'Erro ao carregar lista de produtos.')
        return render(request, 'product/product_list.html', {
            'products': [],
            'search': ''
        })


def product_create(request):
    """Cria um novo produto"""
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Produto cadastrado com sucesso!')
                return redirect('product:product_list')

            except ValidationError as e:
                messages.error(request, f'Erro de validação: {e}')

            except IntegrityError:
                messages.error(request, 'Erro: Produto já existe.')

            except Exception:
                messages.error(request, 'Erro ao cadastrar produto.')

        else:
            messages.error(request, 'Corrija os erros do formulário.')

    else:
        form = ProductForm()

    return render(request, 'product/product_form.html', {
        'form': form,
        'title': 'Cadastrar Produto'
    })


def product_edit(request, id):
    """Edita um produto existente"""
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Produto atualizado com sucesso!')
                return redirect('product:product_list')

            except ValidationError:
                messages.error(request, 'Dados inválidos.')

            except IntegrityError:
                messages.error(request, 'Erro: Já existe um produto com esses dados.')

            except Exception:
                messages.error(request, 'Erro ao atualizar produto.')

        else:
            messages.error(request, 'Corrija os erros do formulário.')

    else:
        form = ProductForm(instance=product)

    return render(request, 'product/product_form.html', {
        'form': form,
        'title': 'Editar Produto',
        'product': product
    })


def product_delete(request, id):
    """Exclui um produto"""
    if request.method not in ['POST', 'DELETE']:
        messages.error(request, 'Ação não permitida.')
        return redirect('product:product_list')

    try:
        product = get_object_or_404(Product, id=id)
        product_name = product.description

        product.delete()
        messages.success(request, f'Produto "{product_name}" excluído com sucesso!')

    except Exception:
        messages.error(request, 'Erro ao excluir produto.')

    return redirect('product:product_list')
