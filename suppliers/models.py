from django.db import models
from django.core.validators import RegexValidator, EmailValidator

class Supplier(models.Model):
    BRAZILIAN_STATES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Federal District'),
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

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    mobile = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$')],
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$')],
        blank=True,
        null=True
    )
    postal_code = models.CharField(max_length=9, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, choices=BRAZILIAN_STATES, blank=True, null=True)
    complement = models.CharField(max_length=100, blank=True, null=True)
    cnpj = models.CharField(
        "CNPJ",
        max_length=18,
        unique=True,
        validators=[RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.cnpj}"
