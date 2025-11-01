from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from functools import wraps
import json
from .models import Employee


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
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def employee_list(request):
    """View para listar todos os funcionários"""
    employees = Employee.objects.all().order_by('username')
    return render(request, 'employees/list.html', {'employees': employees})


@admin_required
@require_http_methods(["POST"])
def employee_create(request):
    """View para criar um novo funcionário via AJAX"""
    try:
        # Parsear dados JSON
        data = json.loads(request.body)
        
        # Validar campos obrigatórios
        if not data.get('username'):
            return JsonResponse({'success': False, 'error': 'Nome é obrigatório'}, status=400)
        
        if not data.get('email'):
            return JsonResponse({'success': False, 'error': 'E-mail é obrigatório'}, status=400)
        
        if not data.get('password'):
            return JsonResponse({'success': False, 'error': 'Senha é obrigatória'}, status=400)
        
        # Verificar se o email já existe
        if Employee.objects.filter(email=data.get('email')).exists():
            return JsonResponse({'success': False, 'error': 'E-mail já cadastrado'}, status=400)
        
        # Criar o funcionário
        employee = Employee.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            phone=data.get('phone', ''),
            mobile=data.get('mobile', ''),
            cpf=data.get('cpf', ''),
            rg=data.get('rg', ''),
            cargo=data.get('cargo', ''),
            access_level=data.get('access_level', 'Usuário'),
            cep=data.get('cep', ''),
            endereco=data.get('endereco', ''),
            numero=data.get('numero') if data.get('numero') else None,
            complemento=data.get('complemento', ''),
            bairro=data.get('bairro', ''),
            cidade=data.get('cidade', ''),
            estado=data.get('estado', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Funcionário cadastrado com sucesso',
            'employee_id': employee.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@admin_required
@require_http_methods(["GET"])
def employee_detail(request, pk):
    """View para obter detalhes de um funcionário via AJAX"""
    try:
        employee = Employee.objects.get(pk=pk)
        
        return JsonResponse({
            'id': employee.id,
            'username': employee.username,
            'email': employee.email,
            'phone': employee.phone or '',
            'mobile': employee.mobile or '',
            'cpf': employee.cpf or '',
            'rg': employee.rg or '',
            'cargo': employee.cargo or '',
            'access_level': employee.access_level,
            'cep': employee.cep or '',
            'endereco': employee.endereco or '',
            'numero': employee.numero,
            'complemento': employee.complemento or '',
            'bairro': employee.bairro or '',
            'cidade': employee.cidade or '',
            'estado': employee.estado or ''
        })
    except Employee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Funcionário não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@admin_required
@require_http_methods(["PUT"])
def employee_update(request, pk):
    """View para atualizar um funcionário via AJAX"""
    try:
        employee = Employee.objects.get(pk=pk)
        data = json.loads(request.body)
        
        # Atualizar campos
        if data.get('username'):
            employee.username = data.get('username')
        if data.get('email'):
            employee.email = data.get('email')
        
        employee.phone = data.get('phone', '')
        employee.mobile = data.get('mobile', '')
        employee.cpf = data.get('cpf', '')
        employee.rg = data.get('rg', '')
        employee.cargo = data.get('cargo', '')
        employee.access_level = data.get('access_level', 'Usuário')
        employee.cep = data.get('cep', '')
        employee.endereco = data.get('endereco', '')
        employee.numero = data.get('numero') if data.get('numero') else None
        employee.complemento = data.get('complemento', '')
        employee.bairro = data.get('bairro', '')
        employee.cidade = data.get('cidade', '')
        employee.estado = data.get('estado', '')
        
        # Atualizar senha se fornecida
        if data.get('password'):
            employee.set_password(data.get('password'))
        
        employee.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Funcionário atualizado com sucesso'
        })
        
    except Employee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Funcionário não encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@admin_required
@require_http_methods(["DELETE"])
def employee_delete(request, pk):
    """View para excluir um funcionário via AJAX"""
    try:
        employee = Employee.objects.get(pk=pk)
        employee.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Funcionário excluído com sucesso'
        })
        
    except Employee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Funcionário não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
