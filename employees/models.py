from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    """
    Modelo para funcionários da empresa.
    Herda de AbstractUser para ter funcionalidades de autenticação.
    """
    
    # Níveis de acesso
    ACCESS_LEVEL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Usuário', 'Usuário'),
    ]
    
    # Adicionar campos personalizados
    phone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        null=True,
        help_text='Telefone fixo'
    )
    
    mobile = models.CharField(
        'Celular',
        max_length=20,
        blank=True,
        null=True,
        help_text='Número do celular'
    )
    
    cpf = models.CharField(
        'CPF',
        max_length=14,
        blank=True,
        null=True,
        help_text='CPF do funcionário'
    )
    
    rg = models.CharField(
        'RG',
        max_length=20,
        blank=True,
        null=True,
        help_text='RG do funcionário'
    )
    
    cargo = models.CharField(
        'Cargo',
        max_length=50,
        blank=True,
        null=True,
        help_text='Cargo do funcionário'
    )
    
    access_level = models.CharField(
        'Nível de Acesso',
        max_length=20,
        choices=ACCESS_LEVEL_CHOICES,
        default='Usuário',
        help_text='Nível de acesso do funcionário no sistema'
    )
    
    # Campos de endereço
    cep = models.CharField(
        'CEP',
        max_length=10,
        blank=True,
        null=True,
        help_text='CEP do funcionário'
    )
    
    endereco = models.CharField(
        'Endereço',
        max_length=200,
        blank=True,
        null=True,
        help_text='Rua/Logradouro'
    )
    
    numero = models.IntegerField(
        'Número',
        blank=True,
        null=True,
        help_text='Número do endereço'
    )
    
    complemento = models.CharField(
        'Complemento',
        max_length=100,
        blank=True,
        null=True,
        help_text='Complemento do endereço'
    )
    
    bairro = models.CharField(
        'Bairro',
        max_length=100,
        blank=True,
        null=True,
        help_text='Bairro'
    )
    
    cidade = models.CharField(
        'Cidade',
        max_length=100,
        blank=True,
        null=True,
        help_text='Cidade'
    )
    
    estado = models.CharField(
        'Estado',
        max_length=2,
        blank=True,
        null=True,
        help_text='UF do estado'
    )
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['username']
    
    def __str__(self):
        return f"{self.username or self.email} - {self.email}"
    
