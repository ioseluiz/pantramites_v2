from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Recordatorio(models.Model):
    TIPO_RECORDATORIO_CHOICES = [
        ('POR_VENCER', 'Por Vencer'),
        ('VENCIDO', 'Vencido'),
    ]
    
    # Usuario al que se le notifica
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recordatorios')
    
    # Contenido genérico para enlazar a cualquier documento (Poliza, Revisado, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    documento = GenericForeignKey('content_type', 'object_id')
    
    tipo = models.CharField(max_length=20, choices=TIPO_RECORDATORIO_CHOICES, verbose_name='Tipo de Recordatorio')
    mensaje = models.TextField(verbose_name='Mensaje de la notificación')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False, verbose_name='Leído')
    enviado_por_correo = models.BooleanField(default=False, verbose_name='Enviado por Correo')

    class Meta:
        verbose_name = 'Recordatorio'
        verbose_name_plural = 'Recordatorios'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Recordatorio {self.tipo} para {self.usuario.email} sobre {self.documento}'
