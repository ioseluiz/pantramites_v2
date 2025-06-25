from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ruc', 'tipo', 'provincia', 'distrito')
    list_filter = ('tipo', 'provincia', 'distrito')
    search_fields = ('nombre', 'ruc')

class CustomUserAdmin(UserAdmin):
    """
    Configuración del admin para el modelo de usuario personalizado.
    """
    model = CustomUser
    # Campos a mostrar en la lista de usuarios
    list_display = ('email', 'first_name', 'last_name', 'empresa', 'is_staff', 'is_active',)
    # Filtros que aparecerán en la barra lateral derecha
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'empresa')
    # Campos por los que se puede buscar
    search_fields = ('email', 'first_name', 'last_name', 'empresa__nombre',)
    # Campos por los que se puede ordenar
    ordering = ('email',)

    # Los fieldsets controlan el layout en las páginas de edición de un usuario existente
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'empresa')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets se usa para la página de creación de un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'empresa', 'password',),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
