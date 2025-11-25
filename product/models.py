from django.db import models
from django.core.exceptions import ValidationError
from suppliers.models import Supplier as Fornecedor
import re


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, verbose_name="Descrição")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    qty_stock = models.IntegerField(verbose_name="Quantidade em estoque")
    supplier = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        db_column='supplier_id',
        verbose_name="Fornecedor"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['description']

    def __str__(self):
        return self.description

    # -----------------------
    # VALIDATIONS
    # -----------------------

    def clean(self):
        """Validações gerais de produto"""
        super().clean()

        # -------- Descrição --------
        if self.description:
            desc = self.description.strip()
            desc = re.sub(r'\s+', ' ', desc)
            if len(desc) < 3:
                raise ValidationError({'description': 'A descrição deve ter pelo menos 3 caracteres.'})
            if len(desc) > 100:
                raise ValidationError({'description': 'A descrição ultrapassa o limite de 100 caracteres.'})
        else:
            raise ValidationError({'description': 'A descrição é obrigatória.'})

        # -------- Preço --------
        if self.price is None:
            raise ValidationError({'price': 'O preço é obrigatório.'})
        if self.price <= 0:
            raise ValidationError({'price': 'O preço deve ser maior que zero.'})

        # -------- Estoque --------
        if self.qty_stock is None:
            raise ValidationError({'qty_stock': 'A quantidade em estoque é obrigatória.'})
        if self.qty_stock < 0:
            raise ValidationError({'qty_stock': 'A quantidade não pode ser negativa.'})
        if self.qty_stock > 99999:
            raise ValidationError({'qty_stock': 'A quantidade é muito alta.'})

        # -------- Fornecedor --------
        if not self.supplier_id:
            raise ValidationError({'supplier': 'Selecione um fornecedor válido.'})

    # -----------------------
    # CLEAN METHODS
    # -----------------------

    def clean_price(self):
        """Garante que o preço esteja correto"""
        if self.price <= 0:
            raise ValidationError("O preço deve ser maior que zero.")
        return round(self.price, 2)

    def clean_qty_stock(self):
        """Valida estoque"""
        if self.qty_stock < 0:
            raise ValidationError("Estoque não pode ser negativo.")
        return self.qty_stock
