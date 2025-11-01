# Generated migration - Cria usuário administrador padrão

from django.db import migrations


def criar_usuario_admin(apps, schema_editor):
    """
    Cria o usuário administrador padrão do sistema
    Email: suporte@upperlav.com.br
    Senha: upperadmin
    """
    Employee = apps.get_model('employees', 'Employee')
    
    # Verifica se já existe um usuário com este email
    if not Employee.objects.filter(email='suporte@upperlav.com.br').exists():
        # Criar o usuário usando o método create_user para criptografar a senha
        # Como estamos em uma migration, precisamos fazer isso manualmente
        from django.contrib.auth.hashers import make_password
        
        Employee.objects.create(
            username='suporte',
            email='suporte@upperlav.com.br',
            password=make_password('upperadmin'),
            first_name='Suporte',
            last_name='UpperLav',
            access_level='Administrador',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        print("Usuario administrador padrao criado com sucesso!")
        print("   Email: suporte@upperlav.com.br")
        print("   Senha: upperadmin")
    else:
        print("Usuario administrador ja existe.")


def reverter_criacao(apps, schema_editor):
    """
    Reverte a criação do usuário administrador (caso necessário)
    """
    Employee = apps.get_model('employees', 'Employee')
    Employee.objects.filter(email='suporte@upperlav.com.br').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_alter_employee_access_level'),
    ]

    operations = [
        migrations.RunPython(criar_usuario_admin, reverter_criacao),
    ]

