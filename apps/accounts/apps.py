from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Cuentas de Usuarios'

    def ready(self):
        # Importar las signals para que se conecten al iniciar la app
        import apps.accounts.signals
