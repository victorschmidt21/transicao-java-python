from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Supplier

Employee = get_user_model()


class SupplierModelTest(TestCase):
    """Testes para o modelo Supplier"""
    
    def setUp(self):
        """Configuração inicial"""
        self.supplier_data = {
            'name': 'Fornecedor Teste Ltda',
            'cnpj': '12.345.678/0001-90',
            'email': 'fornecedor@test.com',
            'mobile': '(11) 98765-4321',
            'phone': '(11) 3456-7890',
            'postal_code': '01310-100',
            'address': 'Av Paulista',
            'neighborhood': 'Bela Vista',
            'city': 'São Paulo',
            'state': 'SP'
        }
    
    def test_create_supplier(self):
        """Testa criação de fornecedor"""
        supplier = Supplier.objects.create(**self.supplier_data)
        self.assertEqual(supplier.name, 'Fornecedor Teste Ltda')
        self.assertEqual(supplier.cnpj, '12.345.678/0001-90')
    
    def test_supplier_str_representation(self):
        """Testa representação em string"""
        supplier = Supplier.objects.create(**self.supplier_data)
        self.assertIn('Fornecedor Teste Ltda', str(supplier))
        self.assertIn('12.345.678/0001-90', str(supplier))
    
    def test_supplier_unique_cnpj(self):
        """Testa CNPJ único"""
        Supplier.objects.create(**self.supplier_data)
        
        # Tentar criar outro com mesmo CNPJ
        duplicate_data = self.supplier_data.copy()
        duplicate_data['email'] = 'outro@test.com'
        
        with self.assertRaises(Exception):
            Supplier.objects.create(**duplicate_data)
    
    def test_supplier_ordering(self):
        """Testa ordenação por nome"""
        Supplier.objects.create(name='Zeta Fornecedor', cnpj='11.111.111/0001-11', email='z@test.com')
        Supplier.objects.create(name='Alpha Fornecedor', cnpj='22.222.222/0001-22', email='a@test.com')
        
        suppliers = Supplier.objects.all()
        self.assertEqual(suppliers[0].name, 'Alpha Fornecedor')
        self.assertEqual(suppliers[1].name, 'Zeta Fornecedor')
    
    def test_supplier_state_choices(self):
        """Testa choices de estado"""
        supplier = Supplier.objects.create(**self.supplier_data)
        self.assertIn(supplier.state, ['SP', 'RJ', 'MG', 'AC', 'AL'])  # Alguns estados válidos


class SupplierViewTest(TestCase):
    """Testes para as views de Supplier"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = Client()
        
        # Criar usuário para autenticação
        self.user = Employee.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Criar fornecedor de teste
        self.supplier = Supplier.objects.create(
            name='Fornecedor Teste',
            cnpj='12.345.678/0001-90',
            email='supplier@test.com'
        )
    
    def test_supplier_list_requires_login(self):
        """Testa que lista requer login"""
        response = self.client.get('/suppliers/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_supplier_list_view(self):
        """Testa view de listagem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/suppliers/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fornecedor Teste', response.content)
