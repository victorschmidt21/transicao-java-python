from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from employees.models import Employee

# Home
def home(request):
    return render(request, 'home.html')


def login_view(request):
    """View para login de usuários"""
    # Se já está autenticado, redireciona
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verificar se o usuário digitou email ou username
        # Se contém @, provavelmente é um email
        if '@' in username_or_email:
            # Buscar o username pelo email
            try:
                employee = Employee.objects.get(email=username_or_email)
                username = employee.username
            except Employee.DoesNotExist:
                username = username_or_email  # Usa o valor digitado mesmo
        else:
            username = username_or_email
        
        # Autentica o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            
            # Redireciona para a página solicitada ou para home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    
    return render(request, 'login.html')


def logout_view(request):
    """View para logout de usuários"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')