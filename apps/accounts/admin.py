from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Empresa

class CustomUserAdmin(UserAdmin):
    """
    Configuración del admin para el modelo de usuario personalizado.
    """
    model = CustomUser
    # Campos a mostrar en la lista de usuarios
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    # Campos por los que se puede buscar
    search_fields = ('email', 'first_name', 'last_name',)
    # Campos por los que se puede ordenar
    ordering = ('email',)

    # Los fieldsets controlan el layout en las páginas de edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets se usa para la página de creación de usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password',),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Empresa)
