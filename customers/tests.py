from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Customer
from .forms import CustomerForm

Employee = get_user_model()


class CustomerModelTest(TestCase):
    """Testes para o modelo Customer"""
    
    def setUp(self):
        """Configuração inicial"""
        self.customer_data = {
            'name': 'João Silva',
            'cpf': '12345678900',
            'email': 'joao@example.com',
            'mobile': '11987654321',
            'zip_code': '01310100',
            'address': 'Rua Augusta',
            'neighborhood': 'Consolação',
            'city': 'São Paulo',
            'state': 'SP',
            'number': 1234
        }
    
    def test_create_customer(self):
        """Testa criação de cliente"""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(customer.name, 'João Silva')
        self.assertEqual(customer.email, 'joao@example.com')
    
    def test_customer_str_representation(self):
        """Testa representação em string"""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(str(customer), 'João Silva')
    
    def test_customer_unique_email(self):
        """Testa email único"""
        Customer.objects.create(**self.customer_data)
        
        # Tentar criar outro com mesmo email
        duplicate_data = self.customer_data.copy()
        duplicate_data['cpf'] = '98765432100'
        
        with self.assertRaises(Exception):
            Customer.objects.create(**duplicate_data)
    
    def test_customer_ordering(self):
        """Testa ordenação por nome"""
        Customer.objects.create(name='Zé', email='ze@test.com')
        Customer.objects.create(name='Ana', email='ana@test.com')
        
        customers = Customer.objects.all()
        self.assertEqual(customers[0].name, 'Ana')
        self.assertEqual(customers[1].name, 'Zé')


class CustomerFormTest(TestCase):
    """Testes para o formulário CustomerForm"""
    
    def test_valid_form(self):
        """Testa formulário válido"""
        form_data = {
            'name': 'Maria Santos',
            'cpf': '12345678900',
            'email': 'maria@example.com',
            'mobile': '11987654321',
            'zip_code': '01310100',
            'address': 'Rua Teste',
            'neighborhood': 'Centro',
            'city': 'São Paulo',
            'state': 'SP',
            'number': 100
        }
        form = CustomerForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_name_required(self):
        """Testa nome obrigatório"""
        form_data = {
            'email': 'test@example.com'
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_name_too_short(self):
        """Testa nome muito curto"""
        form_data = {
            'name': 'A',
            'email': 'test@example.com'
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_cpf_length(self):
        """Testa CPF com tamanho inválido"""
        form_data = {
            'name': 'Test User',
            'cpf': '123',
            'email': 'test@example.com'
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_mobile_length(self):
        """Testa celular com tamanho inválido"""
        form_data = {
            'name': 'Test User',
            'mobile': '123',
            'email': 'test@example.com'
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_zip_code(self):
        """Testa CEP inválido"""
        form_data = {
            'name': 'Test User',
            'zip_code': '123',
            'email': 'test@example.com'
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())


class CustomerViewTest(TestCase):
    """Testes para as views de Customer"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = Client()
        
        # Criar usuário para autenticação
        self.user = Employee.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Criar cliente de teste
        self.customer = Customer.objects.create(
            name='Cliente Teste',
            email='cliente@test.com',
            mobile='11987654321'
        )
    
    def test_customer_list_requires_login(self):
        """Testa que lista requer login"""
        response = self.client.get(reverse('customers:customer_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_list_view(self):
        """Testa view de listagem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('customers:customer_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_list.html')
        self.assertIn('customers', response.context)
    
    def test_customer_list_search(self):
        """Testa busca na listagem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('customers:customer_list'), {'search': 'Cliente'})
        
        self.assertEqual(response.status_code, 200)
        customers = response.context['customers']
        self.assertEqual(customers.count(), 1)
    
    def test_customer_create_view_get(self):
        """Testa GET da view de criação"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('customers:customer_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_form.html')
    
    def test_customer_create_view_post(self):
        """Testa POST da view de criação"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'name': 'Novo Cliente',
            'email': 'novo@test.com',
            'mobile': '11999887766'
        }
        
        response = self.client.post(reverse('customers:customer_create'), data)
        
        # Deve redirecionar
        self.assertEqual(response.status_code, 302)
        
        # Verifica se foi criado
        self.assertTrue(Customer.objects.filter(name='Novo Cliente').exists())
    
    def test_customer_edit_view_get(self):
        """Testa GET da view de edição"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('customers:customer_edit', kwargs={'id': self.customer.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/customer_form.html')
    
    def test_customer_edit_view_post(self):
        """Testa POST da view de edição"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'name': 'Cliente Atualizado',
            'email': 'cliente@test.com',
            'mobile': '11987654321'
        }
        
        response = self.client.post(
            reverse('customers:customer_edit', kwargs={'id': self.customer.id}),
            data
        )
        
        # Deve redirecionar
        self.assertEqual(response.status_code, 302)
        
        # Verifica se foi atualizado
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Cliente Atualizado')
    
    def test_customer_delete_view(self):
        """Testa view de exclusão"""
        self.client.login(username='testuser', password='testpass123')
        
        customer_id = self.customer.id
        response = self.client.post(
            reverse('customers:customer_delete', kwargs={'id': customer_id})
        )
        
        # Deve redirecionar
        self.assertEqual(response.status_code, 302)
        
        # Verifica se foi excluído
        self.assertFalse(Customer.objects.filter(id=customer_id).exists())
