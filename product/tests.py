from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product
from suppliers.models import Supplier

Employee = get_user_model()


# class ProductModelTest(TestCase):
#     """Testes para o modelo Product"""
    
#     def setUp(self):
#         """Configuração inicial"""
#         # Criar fornecedor para relacionamento
#         self.supplier = Supplier.objects.create(
#             name='Fornecedor Teste',
#             cnpj='12.345.678/0001-90',
#             email='supplier@test.com'
#         )
        
#         self.product_data = {
#             'description': 'Produto Teste',
#             'price': 99.90,
#             'qty_stock': 100,
#             'supplier': self.supplier
#         }
    
#     def test_create_product(self):
#         """Testa criação de produto"""
#         product = Product.objects.create(**self.product_data)
#         self.assertEqual(product.description, 'Produto Teste')
#         self.assertEqual(float(product.price), 99.90)
#         self.assertEqual(product.qty_stock, 100)
    
#     def test_product_str_representation(self):
#         """Testa representação em string"""
#         product = Product.objects.create(**self.product_data)
#         self.assertEqual(str(product), 'Produto Teste')
    
#     def test_product_supplier_relationship(self):
#         """Testa relacionamento com fornecedor"""
#         product = Product.objects.create(**self.product_data)
#         self.assertEqual(product.supplier, self.supplier)
#         self.assertEqual(product.supplier.name, 'Fornecedor Teste')
    
#     def test_product_ordering(self):
#         """Testa ordenação por descrição"""
#         Product.objects.create(description='Zebra Product', price=10, qty_stock=5, supplier=self.supplier)
#         Product.objects.create(description='Alpha Product', price=20, qty_stock=10, supplier=self.supplier)
        
#         products = Product.objects.all()
#         self.assertEqual(products[0].description, 'Alpha Product')
#         self.assertEqual(products[1].description, 'Zebra Product')
    
#     def test_product_price_decimal(self):
#         """Testa precisão decimal do preço"""
#         product = Product.objects.create(
#             description='Test',
#             price=123.45,
#             qty_stock=10,
#             supplier=self.supplier
#         )
#         self.assertEqual(float(product.price), 123.45)
    
#     def test_product_stock_update(self):
#         """Testa atualização de estoque"""
#         product = Product.objects.create(**self.product_data)
        
#         # Reduzir estoque
#         product.qty_stock -= 10
#         product.save()
        
#         product.refresh_from_db()
#         self.assertEqual(product.qty_stock, 90)
    
#     def test_product_cascade_delete(self):
#         """Testa exclusão em cascata quando fornecedor é excluído"""
#         product = Product.objects.create(**self.product_data)
#         product_id = product.id
        
#         # Excluir fornecedor
#         self.supplier.delete()
        
#         # Produto deve ser excluído também
#         self.assertFalse(Product.objects.filter(id=product_id).exists())


# class ProductViewTest(TestCase):
#     """Testes para as views de Product"""
    
#     def setUp(self):
#         """Configuração inicial"""
#         self.client = Client()
        
#         # Criar usuário para autenticação
#         self.user = Employee.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='testpass123'
#         )
        
#         # Criar fornecedor
#         self.supplier = Supplier.objects.create(
#             name='Fornecedor Teste',
#             cnpj='12.345.678/0001-90',
#             email='supplier@test.com'
#         )
        
#         # Criar produto de teste
#         self.product = Product.objects.create(
#             description='Produto Teste',
#             price=99.90,
#             qty_stock=50,
#             supplier=self.supplier
#         )
    
#     def test_product_list_requires_login(self):
#         """Testa que lista requer login"""
#         response = self.client.get('/product/')
#         self.assertEqual(response.status_code, 302)  # Redirect to login
    
#     def test_product_list_view(self):
#         """Testa view de listagem"""
#         self.client.login(username='testuser', password='testpass123')
#         response = self.client.get('/product/')
        
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Produto Teste', response.content)
