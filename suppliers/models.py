from django.db import models
from django.core.validators import RegexValidator, EmailValidator

class Fornecedor(models.Model):
    ESTADOS_BRASILEIROS = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    celular = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$')],
        blank=True,
        null=True
    )
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$')],
        blank=True,
        null=True
    )
    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=150, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS_BRASILEIROS, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    cpnj = models.CharField(
        "CNPJ",
        max_length=18,
        unique=True,
        validators=[RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')],
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.cpnj}"

