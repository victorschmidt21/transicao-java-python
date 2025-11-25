from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Product
from .forms import ProductForm
from suppliers.models import Supplier

Employee = get_user_model()


# ----------------------------------------------------
# MODEL TESTS
# ----------------------------------------------------
class ProductModelTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Fornecedor Teste",
            email="fornecedor@teste.com",
            cnpj="12345678000100",
            mobile="11999999999"
        )

        self.product_data = {
            "description": "Produto Teste",
            "price": 10.50,
            "qty_stock": 5,
            "supplier": self.supplier
        }

    def test_create_product(self):
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.description, "Produto Teste")
        self.assertEqual(product.price, 10.50)
        self.assertEqual(product.qty_stock, 5)

    def test_str_representation(self):
        product = Product.objects.create(**self.product_data)
        self.assertEqual(str(product), "Produto Teste")

    def test_invalid_price(self):
        data = self.product_data.copy()
        data["price"] = -10
        with self.assertRaises(ValidationError):
            p = Product(**data)
            p.full_clean()

    def test_invalid_qty_stock(self):
        data = self.product_data.copy()
        data["qty_stock"] = -1
        with self.assertRaises(ValidationError):
            p = Product(**data)
            p.full_clean()

    def test_description_too_short(self):
        data = self.product_data.copy()
        data["description"] = "aa"
        with self.assertRaises(ValidationError):
            p = Product(**data)
            p.full_clean()


# ----------------------------------------------------
# FORM TESTS
# ----------------------------------------------------
class ProductFormTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Fornecedor",
            email="f@f.com",
            cnpj="12345678000100",
            mobile="11999999999"
        )

    def test_valid_form(self):
        form_data = {
            "description": "Produto Bom",
            "price": 20.50,
            "qty_stock": 10,
            "supplier": self.supplier.id
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_description(self):
        form = ProductForm(data={
            "price": 10,
            "qty_stock": 1,
            "supplier": self.supplier.id
        })
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def test_negative_price(self):
        form = ProductForm(data={
            "description": "Produto",
            "price": -5,
            "qty_stock": 1,
            "supplier": self.supplier.id
        })
        self.assertFalse(form.is_valid())

    def test_negative_stock(self):
        form = ProductForm(data={
            "description": "Produto",
            "price": 10,
            "qty_stock": -1,
            "supplier": self.supplier.id
        })
        self.assertFalse(form.is_valid())


# ----------------------------------------------------
# VIEW TESTS
# ----------------------------------------------------
class ProductViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Usuário logado
        self.user = Employee.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Fornecedor
        self.supplier = Supplier.objects.create(
            name="Fornecedor View",
            email="v@test.com",
            cnpj="55555555000100",
            mobile="11999999999"
        )

        # Produto
        self.product = Product.objects.create(
            description="Produto View",
            price=12.99,
            qty_stock=4,
            supplier=self.supplier
        )

    # ---- LIST ----
    def test_product_list_view(self):
        response = self.client.get(reverse("product:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/product_list.html")
        self.assertIn("products", response.context)

    def test_product_list_search(self):
        response = self.client.get(reverse("product:product_list"), {"search": "View"})
        products = response.context["products"]
        self.assertEqual(products.count(), 1)

    # ---- CREATE ----
    def test_product_create_get(self):
        response = self.client.get(reverse("product:product_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/product_form.html")

    def test_product_create_post(self):
        data = {
            "description": "Novo Produto",
            "price": 30.00,
            "qty_stock": 10,
            "supplier": self.supplier.id
        }
        response = self.client.post(reverse("product:product_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(description="Novo Produto").exists())

    # ---- EDIT ----
    def test_product_edit_get(self):
        response = self.client.get(reverse("product:product_edit", kwargs={"id": self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product/product_form.html")

    def test_product_edit_post(self):
        data = {
            "description": "Produto Editado",
            "price": 45.00,
            "qty_stock": 8,
            "supplier": self.supplier.id
        }
        response = self.client.post(reverse("product:product_edit", kwargs={"id": self.product.id}), data)
        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()
        self.assertEqual(self.product.description, "Produto Editado")

    # ---- DELETE ----
    def test_product_delete(self):
        response = self.client.post(reverse("product:product_delete", kwargs={"id": self.product.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
