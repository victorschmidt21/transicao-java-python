from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Order, OrderItem
from customers.models import Customer
from product.models import Product
from suppliers.models import Supplier

Employee = get_user_model()


class OrderModelTest(TestCase):
    """Testes para o modelo Order"""
    
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
    
    def test_create_order(self):
        """Testa criação de pedido"""
        order = Order.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
        self.assertEqual(order.customer, self.customer)
        self.assertIsNotNone(order.order_date)
    
    def test_order_str_representation(self):
        """Testa representação em string"""
        order = Order.objects.create(
            customer=self.customer,
            total_amount=Decimal('150.00')
        )
        self.assertIn('Cliente Teste', str(order))
    
    def test_order_customer_relationship(self):
        """Testa relacionamento com cliente"""
        order = Order.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
        self.assertEqual(order.customer.name, 'Cliente Teste')
    
    def test_order_cascade_delete(self):
        """Testa exclusão em cascata quando cliente é excluído"""
        order = Order.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
        order_id = order.id
        
        # Excluir cliente
        self.customer.delete()
        
        # Pedido deve ser excluído também
        self.assertFalse(Order.objects.filter(id=order_id).exists())


class OrderItemModelTest(TestCase):
    """Testes para o modelo OrderItem"""
    
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
        
        # Criar pedido
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=Decimal('0.00')
        )
    
    def test_create_order_item(self):
        """Testa criação de item de pedido"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            subtotal=Decimal('200.00')
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.subtotal, Decimal('200.00'))
    
    def test_order_item_relationships(self):
        """Testa relacionamentos do item"""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            subtotal=Decimal('100.00')
        )
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product)
    
    def test_order_item_subtotal_calculation(self):
        """Testa cálculo de subtotal"""
        quantity = 3
        expected_subtotal = self.product.price * quantity
        
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=quantity,
            subtotal=expected_subtotal
        )
        self.assertEqual(item.subtotal, expected_subtotal)
    
    def test_order_item_stock_validation(self):
        """Testa validação de estoque"""
        # Produto tem 50 em estoque
        initial_stock = self.product.qty_stock
        
        # Criar item com quantidade válida
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=10,
            subtotal=Decimal('1000.00')
        )
        
        # Verificar que quantidade é válida
        self.assertLessEqual(item.quantity, initial_stock)


class OrderViewTest(TestCase):
    """Testes para as views de Order"""
    
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
        
        # Criar pedido
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=Decimal('100.00')
        )
    
    def test_order_list_requires_login(self):
        """Testa que lista requer login"""
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_order_list_view(self):
        """Testa view de listagem"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/order/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cliente Teste', response.content)
