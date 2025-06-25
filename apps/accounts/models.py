from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from apps.gestion_flota.models import Provincia, Municipio,Corregimiento

# -----------------------------------------------------------------------------
# MODELO EMPRESA
# -----------------------------------------------------------------------------
class Empresa(models.Model):
    TIPO_EMPRESA_CHOICES = [
        ('NATURAL', 'Natural'),
        ('JURIDICA', 'Jurídica'),
    ]
    nombre = models.CharField(max_length=255, unique=True, verbose_name='Nombre de la Empresa')
    ruc = models.CharField(max_length=20, unique=True, verbose_name='RUC')
    tipo = models.CharField(max_length=10, choices=TIPO_EMPRESA_CHOICES, default='JURIDICA', verbose_name='Tipo de Empresa')
    # Direccion
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True, related_name='empresas', verbose_name='Provincia')
    distrito = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, related_name='empresas_por_distrito', verbose_name='Distrito')
    corregimiento = models.ForeignKey(Corregimiento, on_delete=models.SET_NULL, null=True, blank=True, related_name='empresas', verbose_name='Corregimiento')
    calle = models.CharField(max_length=255, blank=True, verbose_name='Calle o Avenida')
    casa = models.CharField(max_length=50, blank=True, verbose_name='Casa o Edificio')
    direccion = models.CharField(max_length=255, blank=True, verbose_name='Dirección')

    # Contacto
    email_1 = models.EmailField(verbose_name='Email Principal')
    email_2 = models.EmailField(blank=True, verbose_name='Email Secundario')
    telefono_1 = models.CharField(max_length=20, verbose_name='Teléfono Principal')
    telefono_2 = models.CharField(max_length=20, blank=True, verbose_name='Teléfono Secundario')

    # Branding
    url_logo_empresa = models.URLField(max_length=255, blank=True, verbose_name='URL del Logo')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        # Asigna automáticamente la provincia basado en el distrito/corregimiento seleccionado
        if self.corregimiento:
            self.distrito = self.corregimiento.municipio
        if self.distrito:
            self.provincia = self.distrito.provincia
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# -----------------------------------------------------------------------------
# MANAGER PARA EL USUARIO PERSONALIZADO
# -----------------------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para nuestro modelo User donde el email es el identificador
    único para la autenticación en lugar de los nombres de usuario.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un Usuario con el email y contraseña dados.
        """
        if not email:
            raise ValueError('El campo Email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un Superusuario con el email y contraseña dados.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # Los superusuarios no necesitan pertenecer a una empresa
        extra_fields.setdefault('empresa', None)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)

# -----------------------------------------------------------------------------
# MODELO DE USUARIO PERSONALIZADO
# -----------------------------------------------------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        related_name='usuarios',
        null=True, # Permitir nulo para superusuarios
        blank=True,
        verbose_name='Empresa'
    )
    email = models.EmailField('dirección de email', unique=True)
    first_name = models.CharField('nombre', max_length=150, blank=True)
    last_name = models.CharField('apellidos', max_length=150, blank=True)
    
    is_staff = models.BooleanField(
        'es staff',
        default=False,
        help_text='Designa si el usuario puede iniciar sesión en el sitio de administración.',
    )
    is_active = models.BooleanField(
        'activo',
        default=True,
        help_text='Designa si este usuario debe ser tratado como activo. Desmarque esto en lugar de eliminar cuentas.',
    )
    date_joined = models.DateTimeField('fecha de registro', default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Devuelve el first_name más el last_name, con un espacio en medio.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Devuelve el nombre corto para el usuario."""
        return self.first_name

# -----------------------------------------------------------------------------
# MODELO DE PERFIL DE USUARIO
# -----------------------------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name='biografía')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='foto de perfil')
    birth_date = models.DateField(null=True, blank=True, verbose_name='fecha de nacimiento')
    
    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return f'Perfil de {self.user.email}'
