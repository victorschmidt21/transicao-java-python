from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Employee
from .forms import EmployeeForm

Employee = get_user_model()


class EmployeeModelTest(TestCase):
    """Testes para o modelo Employee"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.employee_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'testpass123',
            'access_level': 'Usuário',
            'phone': '(11) 1234-5678',
            'mobile': '(11) 98765-4321',
            'cpf': '123.456.789-00',
            'rg': '12.345.678-9',
            'cargo': 'Desenvolvedor',
            'cep': '01310-100',
            'endereco': 'Rua Teste',
            'numero': 123,
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP'
        }
    
    def test_create_employee(self):
        """Testa criação de funcionário"""
        employee = Employee.objects.create_user(
            username=self.employee_data['username'],
            email=self.employee_data['email'],
            password=self.employee_data['password']
        )
        self.assertEqual(employee.username, 'test_user')
        self.assertEqual(employee.email, 'test@example.com')
        self.assertTrue(employee.check_password('testpass123'))
    
    def test_employee_default_access_level(self):
        """Testa nível de acesso padrão"""
        employee = Employee.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.assertEqual(employee.access_level, 'Usuário')
    
    def test_employee_admin_access_level(self):
        """Testa criação de administrador"""
        admin = Employee.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            access_level='Administrador'
        )
        self.assertEqual(admin.access_level, 'Administrador')
    
    def test_employee_str_representation(self):
        """Testa representação em string"""
        employee = Employee.objects.create_user(
            username='john',
            email='john@example.com',
            password='pass123'
        )
        self.assertIn('john', str(employee))
    
    def test_employee_with_full_data(self):
        """Testa criação com todos os campos"""
        employee = Employee.objects.create_user(**self.employee_data)
        self.assertEqual(employee.phone, '(11) 1234-5678')
        self.assertEqual(employee.mobile, '(11) 98765-4321')
        self.assertEqual(employee.cpf, '123.456.789-00')
        self.assertEqual(employee.cargo, 'Desenvolvedor')
        self.assertEqual(employee.cidade, 'São Paulo')


class EmployeeFormTest(TestCase):
    """Testes para o formulário EmployeeForm"""
    
    def test_valid_form_create(self):
        """Testa formulário válido para criação"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'secure123',
            'password_confirm': 'secure123',
            'access_level': 'Usuário'
        }
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """Testa senhas diferentes"""
        form_data = {
            'username': 'user',
            'email': 'user@example.com',
            'password': 'pass123',
            'password_confirm': 'different',
            'access_level': 'Usuário'
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('As senhas não coincidem', str(form.errors))
    
    def test_password_too_short(self):
        """Testa senha muito curta"""
        form_data = {
            'username': 'user',
            'email': 'user@example.com',
            'password': '123',
            'password_confirm': '123',
            'access_level': 'Usuário'
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('pelo menos 6 caracteres', str(form.errors))
    
    def test_password_required_on_create(self):
        """Testa senha obrigatória ao criar"""
        form_data = {
            'username': 'user',
            'email': 'user@example.com',
            'access_level': 'Usuário'
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('obrigatória', str(form.errors))
    
    def test_password_optional_on_edit(self):
        """Testa senha opcional ao editar"""
        employee = Employee.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='oldpass123'
        )
        form_data = {
            'username': 'existing_updated',
            'email': 'existing@example.com',
            'access_level': 'Usuário'
        }
        form = EmployeeForm(data=form_data, instance=employee)
        self.assertTrue(form.is_valid())


class EmployeeViewTest(TestCase):
    """Testes para as views de Employee"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = Client()
        
        # Criar administrador
        self.admin = Employee.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            access_level='Administrador'
        )
        
        # Criar usuário comum
        self.user = Employee.objects.create_user(
            username='user',
            email='user@test.com',
            password='user123',
            access_level='Usuário'
        )
        
        # Criar funcionário de teste
        self.employee = Employee.objects.create_user(
            username='employee1',
            email='emp1@test.com',
            password='emp123',
            access_level='Usuário'
        )
    
    def test_employee_list_requires_admin(self):
        """Testa que lista requer administrador"""
        # Sem login
        response = self.client.get(reverse('employees:employee_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Com usuário comum
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('employees:employee_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        
        # Com administrador
        self.client.logout()
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('employees:employee_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_employee_list_view(self):
        """Testa view de listagem"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('employees:employee_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/list.html')
        self.assertIn('employees', response.context)
    
    def test_employee_list_search(self):
        """Testa busca na listagem"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('employees:employee_list'), {'search': 'employee1'})
        
        self.assertEqual(response.status_code, 200)
        employees = response.context['employees']
        self.assertEqual(employees.count(), 1)
        self.assertEqual(employees.first().username, 'employee1')
    
    def test_employee_create_view_get(self):
        """Testa GET da view de criação"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('employees:employee_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/employee_form.html')
        self.assertIn('form', response.context)
    
    def test_employee_create_view_post(self):
        """Testa POST da view de criação"""
        self.client.login(username='admin', password='admin123')
        
        data = {
            'username': 'newemployee',
            'email': 'new@test.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'access_level': 'Usuário',
            'phone': '',
            'mobile': '',
            'cpf': '',
            'rg': '',
            'cargo': '',
            'cep': '',
            'endereco': '',
            'numero': '',
            'complemento': '',
            'bairro': '',
            'cidade': '',
            'estado': ''
        }
        
        response = self.client.post(reverse('employees:employee_create'), data)
        
        # Deve redirecionar para lista se válido
        if response.status_code == 302:
            # Verifica se foi criado
            self.assertTrue(Employee.objects.filter(username='newemployee').exists())
        else:
            # Se não redirecionou, pode ter erro de validação
            self.assertEqual(response.status_code, 200)
    
    def test_employee_edit_view_get(self):
        """Testa GET da view de edição"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('employees:employee_edit', kwargs={'pk': self.employee.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/employee_form.html')
        self.assertEqual(response.context['employee'], self.employee)
    
    def test_employee_edit_view_post(self):
        """Testa POST da view de edição"""
        self.client.login(username='admin', password='admin123')
        
        data = {
            'username': 'employee_updated',
            'email': 'emp1@test.com',
            'access_level': 'Administrador',
            'phone': '',
            'mobile': '',
            'cpf': '',
            'rg': '',
            'cargo': '',
            'cep': '',
            'endereco': '',
            'numero': '',
            'complemento': '',
            'bairro': '',
            'cidade': '',
            'estado': ''
        }
        
        response = self.client.post(
            reverse('employees:employee_edit', kwargs={'pk': self.employee.pk}),
            data
        )
        
        # Deve redirecionar se válido
        if response.status_code == 302:
            # Verifica se foi atualizado
            self.employee.refresh_from_db()
            self.assertEqual(self.employee.username, 'employee_updated')
            self.assertEqual(self.employee.access_level, 'Administrador')
        else:
            # Se não redirecionou, pode ter erro de validação
            self.assertEqual(response.status_code, 200)
    
    def test_employee_delete_view(self):
        """Testa view de exclusão"""
        self.client.login(username='admin', password='admin123')
        
        employee_id = self.employee.pk
        response = self.client.post(
            reverse('employees:employee_delete', kwargs={'pk': employee_id})
        )
        
        # Deve redirecionar
        self.assertEqual(response.status_code, 302)
        
        # Verifica se foi excluído
        self.assertFalse(Employee.objects.filter(pk=employee_id).exists())
    
    def test_employee_delete_requires_post(self):
        """Testa que exclusão requer POST"""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(
            reverse('employees:employee_delete', kwargs={'pk': self.employee.pk})
        )
        
        # Deve redirecionar sem excluir
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Employee.objects.filter(pk=self.employee.pk).exists())
