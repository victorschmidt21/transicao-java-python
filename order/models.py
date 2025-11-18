from django.db import models
from django.utils import timezone 

from product.models import Product
from customers.models import Customer
# Create your models here.

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        db_column='customer_id'
    )
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['order_date']


    def __str__(self):
        return f"Order #{self.id} - Customer: {self.customer}"
    
class OrderItem(models.Model):
        id = models.AutoField(primary_key=True)
        order = models.ForeignKey(
            Order,
            on_delete=models.CASCADE,
            db_column='order_id',
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
            verbose_name = "OrderItem"
            verbose_name_plural = "OrderItems"
            ordering = ['id']

        def __str__(self):
            return f"{self.quantity}x {self.product.description} (Order #{self.order.id})"