from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from suppliers.models import Supplier
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'price', 'qty_stock', 'supplier']
        widgets = {
        'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Descrição'}),
        'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Preço'}),
        'qty_stock': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Quantidade de estoque'}),
        'supplier': forms.Select(attrs={'class': 'form-control-select'})
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # garantir placeholder e required
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['qty_stock'].required = True
        self.fields['supplier'].required = True


    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        desc_clean = re.sub(r'\s+', ' ', desc).strip()
        if len(desc_clean) < 3:
            raise ValidationError('Descrição muito curta')
        return desc_clean


    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError('Preço é obrigatório')
        if price <= 0:
            raise ValidationError('Preço deve ser maior que zero')
        return round(price, 2)


    def clean_qty_stock(self):
        qty = self.cleaned_data.get('qty_stock')
        if qty is None:
            raise ValidationError('Quantidade é obrigatória')
        if qty < 0:
            raise ValidationError('Quantidade não pode ser negativa')
        if qty > 99999:
            raise ValidationError('Quantidade muito alta')
        return qty


    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')
        if not supplier:
            raise ValidationError('Fornecedor inválido')
        return supplier