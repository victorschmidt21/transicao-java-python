from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee


class EmployeeForm(forms.ModelForm):
    """Form para criar e editar funcionários"""
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        required=False,
        help_text='Deixe em branco para manter a senha atual (apenas ao editar)'
    )
    
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        required=False
    )
    
    class Meta:
        model = Employee
        fields = [
            'username', 'email', 'phone', 'mobile',
            'cpf', 'rg', 'cargo', 'access_level',
            'cep', 'endereco', 'numero', 'complemento',
            'bairro', 'cidade', 'estado'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'access_level': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'phone': 'Telefone',
            'mobile': 'Celular',
            'cpf': 'CPF',
            'rg': 'RG',
            'cargo': 'Cargo',
            'access_level': 'Nível de Acesso',
            'cep': 'CEP',
            'endereco': 'Endereço',
            'numero': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Se está criando (não tem instance.pk) ou se preencheu senha
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('As senhas não coincidem')
            
            if len(password) < 6:
                raise forms.ValidationError('A senha deve ter pelo menos 6 caracteres')
        
        # Se está criando, senha é obrigatória
        if not self.instance.pk and not password:
            raise forms.ValidationError('Senha é obrigatória ao criar um novo funcionário')
        
        return cleaned_data
    
    def save(self, commit=True):
        employee = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        # Se forneceu senha, atualiza
        if password:
            employee.set_password(password)
        
        # Se está criando e não tem senha definida, usar uma padrão
        if not employee.pk and not password:
            employee.set_password('changeme123')
        
        if commit:
            employee.save()
        
        return employee
