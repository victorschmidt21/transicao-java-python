from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    """
    Modelo para funcionários da empresa.
    Herda de AbstractUser para ter funcionalidades de autenticação.
    """
    
    # Validações personalizadas
    cpf_validator = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message='CPF deve estar no formato: 000.000.000-00'
    )
    
    rg_validator = RegexValidator(
        regex=r'^\d{1,2}\.\d{3}\.\d{3}-\d{1}$',
        message='RG deve estar no formato: 00.000.000-0'
    )
    
    phone_validator = RegexValidator(
        regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
        message='Telefone deve estar no formato: (00) 0000-0000'
    )
    
    mobile_validator = RegexValidator(
        regex=r'^\(\d{2}\)\s\d{5}-\d{4}$',
        message='Celular deve estar no formato: (00) 00000-0000'
    )
    
    # Níveis de acesso
    ACCESS_LEVEL_CHOICES = [
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('employee', 'Funcionário'),
        ('intern', 'Estagiário'),
    ]
    
    # Campos do formulário
    name = models.CharField(
        'Nome',
        max_length=100,
        help_text='Nome completo do funcionário'
    )
    
    email = models.EmailField(
        'E-mail',
        unique=True,
        help_text='E-mail único do funcionário'
    )
    
    phone = models.CharField(
        'Telefone',
        max_length=15,
        validators=[phone_validator],
        blank=True,
        null=True,
        help_text='Telefone fixo'
    )
    
    mobile = models.CharField(
        'Celular',
        max_length=15,
        validators=[mobile_validator],
        help_text='Número do celular'
    )
    
    cpf = models.CharField(
        'CPF',
        max_length=14,
        unique=True,
        validators=[cpf_validator],
        help_text='CPF no formato 000.000.000-00'
    )
    
    rg = models.CharField(
        'RG',
        max_length=12,
        validators=[rg_validator],
        help_text='RG no formato 00.000.000-0'
    )
    
    access_level = models.CharField(
        'Nível de Acesso',
        max_length=10,
        choices=ACCESS_LEVEL_CHOICES,
        default='employee',
        help_text='Nível de acesso do funcionário no sistema'
    )
    
    # Campos de auditoria
    created_at = models.DateTimeField(
        'Data de Criação',
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        'Data de Atualização',
        auto_now=True
    )
    
    is_active = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Indica se o funcionário está ativo'
    )
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    def clean(self):
        """Validações adicionais do modelo"""
        from django.core.exceptions import ValidationError
        
        # Validação de CPF (básica)
        if self.cpf:
            cpf_digits = ''.join(filter(str.isdigit, self.cpf))
            if len(cpf_digits) != 11:
                raise ValidationError({'cpf': 'CPF deve ter 11 dígitos'})
        
        # Validação de RG (básica)
        if self.rg:
            rg_digits = ''.join(filter(str.isdigit, self.rg))
            if len(rg_digits) < 7 or len(rg_digits) > 9:
                raise ValidationError({'rg': 'RG deve ter entre 7 e 9 dígitos'})
    
    def save(self, *args, **kwargs):
        """Override do save para aplicar validações"""
        self.clean()
        super().save(*args, **kwargs)
