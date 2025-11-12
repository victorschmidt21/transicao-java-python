from django.db import models
from django.utils import timezone 

from product.models import Product
from customers.models import Customer
# Create your models here.

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        db_column='customer_id'
    )
    budget_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        ordering = ['budget_date']


    def __str__(self):
        return f"Sale #{self.id} - Customer: {self.customer}"

class BudgetItem(models.Model):
    id = models.AutoField(primary_key=True)
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        db_column='budget_id',
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column='product_id'
    )
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "BudgetItem"
        verbose_name_plural = "BudgetItems"
        ordering = ['id']

    def __str__(self):
        return f"{self.quantity}x {self.product.description} (Sale #{self.sale.id})"
