from django import forms
from django.core.exceptions import ValidationError
from .models import Customer
import re

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'cpf', 'email', 'mobile', 'zip_code', 'address', 
            'neighborhood', 'city', 'state', 'number'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-input',
                'maxlength': '15'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-input',
                'maxlength': '9'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input'
            }),
            'number': forms.NumberInput(attrs={
                'class': 'form-input'
            }),
            'neighborhood': forms.TextInput(attrs={
                'class': 'form-input'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input'
            }),
            'state': forms.Select(attrs={
                'class': 'form-input'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-input',
                'maxlength': '14'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estados brasileiros
        STATE_CHOICES = [
            ('', 'Selecione o estado'),
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
        
        self.fields['state'].widget = forms.Select(choices=STATE_CHOICES, attrs={
            'class': 'form-input'
        })
        
        # Add required field indicators
        self.fields['name'].required = True
        self.fields['name'].error_messages = {
            'required': 'Nome é obrigatório',
            'max_length': 'Nome muito longo'
        }
    
    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Nome é obrigatório')
        if len(name.strip()) < 2:
            raise ValidationError('Nome muito curto')
        return name.strip()
    
    def clean_cpf(self):
        """Validate CPF field"""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove non-numeric characters
            cpf_clean = re.sub(r'\D', '', cpf)
            
            # Check if it has 11 digits
            if len(cpf_clean) != 11:
                raise ValidationError('CPF deve ter 11 dígitos')
            
            # Check if all digits are the same
            if cpf_clean == cpf_clean[0] * 11:
                raise ValidationError('CPF inválido')
            
            # Validate CPF algorithm
            if not self._validate_cpf_algorithm(cpf_clean):
                raise ValidationError('CPF inválido')
            
            return cpf_clean
        return cpf
    
    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already in use by another customer
            if self.instance.pk:
                if Customer.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('E-mail já existe')
            else:
                if Customer.objects.filter(email=email).exists():
                    raise ValidationError('E-mail já existe')
        return email
    
    def clean_mobile(self):
        """Validate mobile field"""
        mobile = self.cleaned_data.get('mobile')
        if mobile:
            # Remove non-numeric characters
            mobile_clean = re.sub(r'\D', '', mobile)
            
            # Check if it has 10 or 11 digits
            if len(mobile_clean) not in [10, 11]:
                raise ValidationError('Celular inválido')
            
            # Check if it starts with valid area code for 11 digits
            if len(mobile_clean) == 11:
                valid_area_codes = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '24', '27', '28', '31', '32', '33', '34', '35', '37', '38', '41', '42', '43', '44', '45', '46', '47', '48', '49', '51', '53', '54', '55', '61', '62', '63', '64', '65', '66', '67', '68', '69', '71', '73', '74', '75', '77', '79', '81', '82', '83', '84', '85', '86', '87', '88', '89', '91', '92', '93', '94', '95', '96', '97', '98', '99']
                if not any(mobile_clean.startswith(code) for code in valid_area_codes):
                    raise ValidationError('DDD inválido')
            
            return mobile_clean
        return mobile
    
    def clean_zip_code(self):
        """Validate ZIP code field"""
        zip_code = self.cleaned_data.get('zip_code')
        if zip_code:
            # Remove non-numeric characters
            zip_code_clean = re.sub(r'\D', '', zip_code)
            
            # Check if it has 8 digits
            if len(zip_code_clean) != 8:
                raise ValidationError('CEP inválido')
            
            return zip_code_clean
        return zip_code
    
    def clean_number(self):
        """Validate number field"""
        number = self.cleaned_data.get('number')
        if number is not None:
            if number < 1:
                raise ValidationError('Número inválido')
            if number > 99999:
                raise ValidationError('Número muito grande')
        return number
    
    def _validate_cpf_algorithm(self, cpf):
        """Validate CPF using the official algorithm"""
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
