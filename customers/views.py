from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Customer
from .forms import CustomerForm

def customer_list(request):
    """Lista todos os clientes"""
    try:
        customers = Customer.objects.all()
        
        # Filtro por pesquisa
        search = request.GET.get('search', '')
        if search:
            customers = customers.filter(name__icontains=search)
        
        context = {
            'customers': customers,
            'search': search
        }
        return render(request, 'customers/customer_list.html', context)
        
    except Exception as e:
        messages.error(request, 'Erro ao carregar lista de clientes')
        return render(request, 'customers/customer_list.html', {'customers': []})

def customer_create(request):
    """Cria um novo cliente"""
    if request.method == 'POST':
        try:
            form = CustomerForm(request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Cliente cadastrado com sucesso!')
                return redirect('customers:customer_list')
                
        except ValidationError as e:
            messages.error(request, 'Dados inválidos')
            
        except IntegrityError as e:
            messages.error(request, 'Cliente já existe')
            
        except Exception as e:
            messages.error(request, 'Erro ao cadastrar cliente')
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'title': 'Cadastrar Cliente'
    }
    return render(request, 'customers/customer_form.html', context)

def customer_edit(request, id):
    """Edita um cliente existente"""
    try:
        customer = get_object_or_404(Customer, id=id)
        
        if request.method == 'POST':
            try:
                form = CustomerForm(request.POST, instance=customer)
                
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Cliente atualizado com sucesso!')
                    return redirect('customers:customer_list')
                    
            except ValidationError as e:
                messages.error(request, 'Dados inválidos')
                
            except IntegrityError as e:
                messages.error(request, 'Dados já existem')
                
            except Exception as e:
                messages.error(request, 'Erro ao atualizar cliente')
        else:
            form = CustomerForm(instance=customer)
        
        context = {
            'form': form,
            'title': 'Editar Cliente',
            'customer': customer
        }
        return render(request, 'customers/customer_form.html', context)
        
    except Exception as e:
        messages.error(request, 'Cliente não encontrado')
        return redirect('customers:customer_list')

def customer_delete(request, id):
    """Exclui um cliente"""
    if request.method not in ['POST', 'DELETE']:
        messages.error(request, 'Acesso negado')
        return redirect('customers:customer_list')
    
    try:
        customer = get_object_or_404(Customer, id=id)
        customer_name = customer.name
        customer.delete()
        messages.success(request, f'Cliente {customer_name} excluído com sucesso!')
        
    except Exception as e:
        messages.error(request, 'Erro ao excluir cliente')
    
    return redirect('customers:customer_list')
