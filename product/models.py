from django.db import models
from suppliers.models import Supplier as Fornecedor

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty_stock = models.IntegerField()
    supplier = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        db_column='supplier_id'  # mantém o mesmo nome da coluna no banco
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['description']

    def __str__(self):
        return self.description