from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Budget, BudgetItem
from customers.models import Customer
from product.models import Product
from suppliers.models import Supplier

Employee = get_user_model()


class BudgetModelTest(TestCase):
    """Testes para o modelo Budget"""
    
    def setUp(self):
        """Configuração inicial"""
        # Criar cliente
        self.customer = Customer.objects.create(
            name='Cliente Teste',
            email='cliente@test.com'
        )
        
        # Criar fornecedor
        self.supplier = Supplier.objects.create(
            name='Fornecedor Teste',
            cnpj='12.345.678/0001-90',
            email='supplier@test.com'
        )
        
        # Criar produtos
        self.product1 = Product.objects.create(
            description='Produto 1',
            price=Decimal('100.00'),
            qty_stock=50,
            supplier=self.supplier
        )
        
        self.product2 = Product.objects.create(
            description='Produto 2',
            price=Decimal('50.00'),
            qty_stock=30,
            supplier=self.supplier
        )
    
    def test_create_budget(self):
        """Testa criação de orçamento"""
        budget = Budget.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
        self.assertEqual(budget.customer, self.customer)
        self.assertIsNotNone(budget.budget_date)
    
    def test_budget_str_representation(self):
        """Testa representação em string"""
        budget = Budget.objects.create(
            customer=self.customer,
            total_amount=Decimal('100.00')
        )
        self.assertIn('Cliente Teste', str(budget))
    
    def test_budget_customer_relationship(self):
        """Testa relacionamento com cliente"""
        budget = Budget.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
        self.assertEqual(budget.customer.name, 'Cliente Teste')
    
    def test_budget_cascade_delete(self):
        """Testa exclusão em cascata quando cliente é excluído"""
        budget = Budget.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
        budget_id = budget.id
        
        # Excluir cliente
        self.customer.delete()
        
        # Orçamento deve ser excluído também
        self.assertFalse(Budget.objects.filter(id=budget_id).exists())


class BudgetItemModelTest(TestCase):
    """Testes para o modelo BudgetItem"""
    
    def setUp(self):
        """Configuração inicial"""
        # Criar cliente
        self.customer = Customer.objects.create(
            name='Cliente Teste',
            email='cliente@test.com'
        )
        
        # Criar fornecedor
        self.supplier = Supplier.objects.create(
            name='Fornecedor Teste',
            cnpj='12.345.678/0001-90',
            email='supplier@test.com'
        )
        
        # Criar produto
        self.product = Product.objects.create(
            description='Produto Teste',
            price=Decimal('100.00'),
            qty_stock=50,
            supplier=self.supplier
        )
        
        # Criar orçamento
        self.budget = Budget.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
    
    def test_create_budget_item(self):
        """Testa criação de item de orçamento"""
        item = BudgetItem.objects.create(
            budget=self.budget,
            product=self.product,
            quantity=2,
            subtotal=Decimal('200.00')
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.subtotal, Decimal('200.00'))
    
    def test_budget_item_relationships(self):
        """Testa relacionamentos do item"""
        item = BudgetItem.objects.create(
            budget=self.budget,
            product=self.product,
            quantity=1,
            subtotal=Decimal('100.00')
        )
        self.assertEqual(item.budget, self.budget)
        self.assertEqual(item.product, self.product)
    
    def test_budget_item_subtotal_calculation(self):
        """Testa cálculo de subtotal"""
        quantity = 3
        expected_subtotal = self.product.price * quantity
        
        item = BudgetItem.objects.create(
            budget=self.budget,
            product=self.product,
            quantity=quantity,
            subtotal=expected_subtotal
        )
        self.assertEqual(item.subtotal, expected_subtotal)


class BudgetViewTest(TestCase):
    """Testes para as views de Budget"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = Client()
        
        # Criar usuário para autenticação
        self.user = Employee.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Criar cliente
        self.customer = Customer.objects.create(
            name='Cliente Teste',
            email='cliente@test.com'
        )
        
        # Criar fornecedor
        self.supplier = Supplier.objects.create(
            name='Fornecedor Teste',
            cnpj='12.345.678/0001-90',
            email='supplier@test.com'
        )
        
        # Criar produto
        self.product = Product.objects.create(
            description='Produto Teste',
            price=Decimal('100.00'),
            qty_stock=50,
            supplier=self.supplier
        )
        
        # Criar orçamento
        self.budget = Budget.objects.create(
            customer=self.customer,
            total_amount=Decimal('100.00')
        )
    
    def test_budget_list_requires_login(self):
        """Testa que lista requer login"""
        response = self.client.get('/budget/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_budget_list_view(self):
        """Testa view de listagem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/budget/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cliente Teste', response.content)
