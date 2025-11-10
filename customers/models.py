from django.db import models
from django.core.exceptions import ValidationError
import re

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    cpf = models.CharField(max_length=14, verbose_name="CPF", blank=True, null=True, unique=True)
    email = models.EmailField(max_length=200, verbose_name="E-mail", blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=15, verbose_name="Celular", blank=True, null=True)
    zip_code = models.CharField(max_length=9, verbose_name="CEP", blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name="Endereço", blank=True, null=True)
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Cidade", blank=True, null=True)
    state = models.CharField(max_length=2, verbose_name="Estado", blank=True, null=True)
    number = models.IntegerField(verbose_name="Número", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        # Validate name
        if self.name and len(self.name.strip()) < 2:
            raise ValidationError({'name': 'Nome deve ter pelo menos 2 caracteres'})
        # Validate CPF if provided
        if self.cpf:
            if not self._validate_cpf(self.cpf):
                raise ValidationError({'cpf': 'Formato de CPF inválido'})
        # Validate mobile if provided
        if self.mobile:
            if not self._validate_mobile(self.mobile):
                raise ValidationError({'mobile': 'Formato de celular inválido'})
        # Validate ZIP code if provided
        if self.zip_code:
            if not self._validate_zip_code(self.zip_code):
                raise ValidationError({'zip_code': 'Formato de CEP inválido'})
    
    def _validate_cpf(self, cpf):
        """Validate Brazilian CPF format"""
        # Remove non-numeric characters
        cpf = re.sub(r'\D', '', cpf)
        
        # Check if it has 11 digits
        if len(cpf) != 11:
            return False
        
        # Check if all digits are the same
        if cpf == cpf[0] * 11:
            return False
        
        # Validate CPF algorithm
        def calculate_digit(cpf_digits, weights):
            sum_result = sum(int(digit) * weight for digit, weight in zip(cpf_digits, weights))
            remainder = sum_result % 11
            return 0 if remainder < 2 else 11 - remainder
        
        try:
            # Calculate first digit
            first_digit = calculate_digit(cpf[:9], range(10, 1, -1))
            if int(cpf[9]) != first_digit:
                return False
            
            # Calculate second digit
            second_digit = calculate_digit(cpf[:10], range(11, 1, -1))
            if int(cpf[10]) != second_digit:
                return False
            
            return True
        except (ValueError, IndexError):
            return False
    
    def _validate_mobile(self, mobile):
        """Validate Brazilian mobile format"""
        # Remove non-numeric characters
        mobile = re.sub(r'\D', '', mobile)
        
        # Check if it has 10 or 11 digits
        if len(mobile) not in [10, 11]:
            return False
        
        # Check if it starts with valid area code
        if len(mobile) == 11:
            valid_area_codes = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '24', '27', '28', '31', '32', '33', '34', '35', '37', '38', '41', '42', '43', '44', '45', '46', '47', '48', '49', '51', '53', '54', '55', '61', '62', '63', '64', '65', '66', '67', '68', '69', '71', '73', '74', '75', '77', '79', '81', '82', '83', '84', '85', '86', '87', '88', '89', '91', '92', '93', '94', '95', '96', '97', '98', '99']
            if not any(mobile.startswith(code) for code in valid_area_codes):
                return False
        
        return True
    
    def _validate_zip_code(self, zip_code):
        """Validate Brazilian ZIP code format"""
        # Remove non-numeric characters
        zip_code = re.sub(r'\D', '', zip_code)
        
        # Check if it has 8 digits
        if len(zip_code) != 8:
            return False
        
        return True
