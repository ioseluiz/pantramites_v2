# Generated by Django 5.2.3 on 2025-06-25 14:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Nombre de la Empresa')),
                ('ruc', models.CharField(max_length=20, unique=True, verbose_name='RUC')),
                ('tipo', models.CharField(choices=[('NATURAL', 'Natural'), ('JURIDICA', 'Jurídica')], default='JURIDICA', max_length=10, verbose_name='Tipo de Empresa')),
                ('calle', models.CharField(blank=True, max_length=255, verbose_name='Calle o Avenida')),
                ('casa', models.CharField(blank=True, max_length=50, verbose_name='Casa o Edificio')),
                ('direccion', models.CharField(blank=True, max_length=255, verbose_name='Dirección')),
                ('email_1', models.EmailField(max_length=254, verbose_name='Email Principal')),
                ('email_2', models.EmailField(blank=True, max_length=254, verbose_name='Email Secundario')),
                ('telefono_1', models.CharField(max_length=20, verbose_name='Teléfono Principal')),
                ('telefono_2', models.CharField(blank=True, max_length=20, verbose_name='Teléfono Secundario')),
                ('url_logo_empresa', models.URLField(blank=True, max_length=255, verbose_name='URL del Logo')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='biografía')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='foto de perfil')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='dirección de email')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='nombre')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='apellidos')),
                ('is_staff', models.BooleanField(default=False, help_text='Designa si el usuario puede iniciar sesión en el sitio de administración.', verbose_name='es staff')),
                ('is_active', models.BooleanField(default=True, help_text='Designa si este usuario debe ser tratado como activo. Desmarque esto en lugar de eliminar cuentas.', verbose_name='activo')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='fecha de registro')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
            },
        ),
    ]
