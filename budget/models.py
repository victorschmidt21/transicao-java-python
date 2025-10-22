from django.db import models

# Create your models here.

class Budget(models.Model):
    client_id = models.IntegerField()
    total_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class BudgetItem(models.Model):
    budget_id = models.ForeignKey(Budget, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity_product = models.IntegerField()
    total_value = models.FloatField()