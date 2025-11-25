from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import Employee
from .forms import EmployeeForm


def admin_required(view_func):
    """
    Decorador personalizado que verifica se o usuário está autenticado
    e se possui nível de acesso 'Administrador'
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Primeiro verifica se está autenticado
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verifica se é administrador
        if request.user.access_level != 'Administrador':
            messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def employee_list(request):
    """View para listar todos os funcionários"""
    try:
        employees = Employee.objects.all().order_by('username')
        
        # Filtro por pesquisa
        search = request.GET.get('search', '')
        if search:
            employees = employees.filter(username__icontains=search)
        
        context = {
            'employees': employees,
            'search': search
        }
        return render(request, 'employees/list.html', context)
    
    except Exception as e:
        messages.error(request, 'Erro ao carregar lista de funcionários')
        return render(request, 'employees/list.html', {'employees': []})


@admin_required
def employee_create(request):
    """View para criar um novo funcionário"""
    if request.method == 'POST':
        try:
            form = EmployeeForm(request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Funcionário cadastrado com sucesso!')
                return redirect('employee_list')
        
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar funcionário: {str(e)}')
    
    else:
        form = EmployeeForm()
    
    context = {
        'form': form,
        'title': 'Cadastrar Funcionário'
    }
    return render(request, 'employees/employee_form.html', context)


@admin_required
def employee_edit(request, pk):
    """View para editar um funcionário existente"""
    try:
        employee = get_object_or_404(Employee, pk=pk)
        
        if request.method == 'POST':
            try:
                form = EmployeeForm(request.POST, instance=employee)
                
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Funcionário atualizado com sucesso!')
                    return redirect('employee_list')
            
            except Exception as e:
                messages.error(request, f'Erro ao atualizar funcionário: {str(e)}')
        
        else:
            form = EmployeeForm(instance=employee)
        
        context = {
            'form': form,
            'title': 'Editar Funcionário',
            'employee': employee
        }
        return render(request, 'employees/employee_form.html', context)
    
    except Exception as e:
        messages.error(request, 'Funcionário não encontrado')
        return redirect('employee_list')


@admin_required
def employee_delete(request, pk):
    """View para excluir um funcionário"""
    if request.method not in ['POST', 'DELETE']:
        messages.error(request, 'Método não permitido')
        return redirect('employee_list')
    
    try:
        employee = get_object_or_404(Employee, pk=pk)
        employee_name = employee.username
        employee.delete()
        messages.success(request, f'Funcionário {employee_name} excluído com sucesso!')
    
    except Exception as e:
        messages.error(request, 'Erro ao excluir funcionário')
    
    return redirect('employee_list')
