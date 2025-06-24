from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from apps.gestion_flota.models import Poliza, RevisadoVehicular, TarjetaPesosDimensiones, Vehiculo
from apps.recordatorios.models import Recordatorio

class Command(BaseCommand):
    help = 'Actualiza el estado de los documentos y placas, y genera recordatorios.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando la actualización de estados y creación de recordatorios...'))
        
        today = timezone.now().date()
        un_mes_adelante = today + timedelta(days=30)

        self.procesar_modelo(Poliza, today, un_mes_adelante)
        self.procesar_modelo(RevisadoVehicular, today, un_mes_adelante)
        self.procesar_modelo(TarjetaPesosDimensiones, today, un_mes_adelante)

        self.stdout.write(self.style.SUCCESS('¡Proceso completado!'))

    def procesar_modelo(self, modelo, today, un_mes_adelante):
        nombre_modelo = modelo._meta.verbose_name_plural.title()
        
        # --- Actualizar a VENCIDO y crear recordatorio ---
        for item in modelo.objects.filter(fecha_vencimiento__lt=today, estado__in=['VIGENTE', 'POR_VENCER']):
            item.estado = 'VENCIDO'
            item.save()
            self.crear_recordatorio(item, 'VENCIDO', f'El documento "{item}" ha vencido.')
            self.stdout.write(f'  - VENCIDO: {item}')

        # --- Actualizar a POR_VENCER y crear recordatorio ---
        for item in modelo.objects.filter(fecha_vencimiento__gte=today, fecha_vencimiento__lte=un_mes_adelante, estado='VIGENTE'):
            item.estado = 'POR_VENCER'
            item.save()
            self.crear_recordatorio(item, 'POR_VENCER', f'El documento "{item}" está por vencer el {item.fecha_vencimiento}.')
            self.stdout.write(f'  - POR VENCER: {item}')

        # --- Actualizar a VIGENTE (y opcionalmente eliminar recordatorios antiguos) ---
        for item in modelo.objects.filter(fecha_vencimiento__gt=un_mes_adelante, estado__in=['POR_VENCER', 'VENCIDO']):
            item.estado = 'VIGENTE'
            item.save()
            # Opcional: Eliminar recordatorios asociados si ya no son necesarios
            content_type = ContentType.objects.get_for_model(item)
            Recordatorio.objects.filter(content_type=content_type, object_id=item.id).delete()
            self.stdout.write(f'  - VIGENTE (renovado): {item}')

    def crear_recordatorio(self, documento, tipo, mensaje):
        """Crea un recordatorio si no existe uno igual reciente."""
        if not hasattr(documento.vehiculo, 'propietario') or not documento.vehiculo.propietario:
            return # No se puede crear recordatorio si no hay propietario

        content_type = ContentType.objects.get_for_model(documento)
        
        # Evita duplicados: no crea un nuevo recordatorio si ya existe uno del mismo tipo para el mismo objeto
        Recordatorio.objects.get_or_create(
            usuario=documento.vehiculo.propietario,
            content_type=content_type,
            object_id=documento.id,
            tipo=tipo,
            defaults={'mensaje': mensaje}
        )

