from django.db import models

import os
from django.core.exceptions import ValidationError
from apps.gestion_flota.models import (
    Vehiculo,
    Poliza,
    RevisadoVehicular,
    TarjetaPesosDimensiones
)

def validate_pdf(value):
    """Validador para asegurar que el archivo subido sea un PDF."""
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError('Solo se permiten archivos en formato PDF.')
    

class FotoVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='fotos')
    foto = models.ImageField(upload_to='guantera/fotos/', verbose_name='Archivo Foto')
    descripcion = models.CharField(max_length=255, blank=True, verbose_name='Descripcion')
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')

    class Meta:
        verbose_name = 'Foto de Vehículo'
        verbose_name_plural = 'Fotos de Vehículos'
        ordering = ['-fecha_carga']

    def __str__(self):
        return f'Foto para {self.vehiculo.placa} - {self.fecha_carga.strftime("%d/%m/%Y")}'
    
class RegistroUnicoVehicular(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, related_name='registro_unico')
    archivo_pdf = models.FileField(
        upload_to='guantera/registros/', 
        validators=[validate_pdf],
        verbose_name='Archivo PDF del Registro'
    )
    fecha_emision = models.DateField(verbose_name='Fecha de Emisión del Documento')
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')

    class Meta:
        verbose_name = 'Registro Único Vehicular'
        verbose_name_plural = 'Registros Únicos Vehiculares'

    def __str__(self):
        return f'Registro Único para {self.vehiculo.placa}'
    
class CopiaRevisadoVehicular(models.Model):
    revisado = models.ForeignKey(RevisadoVehicular, on_delete=models.CASCADE, related_name='copias_documento')
    archivo_pdf = models.FileField(
        upload_to='guantera/revisados/',
        validators=[validate_pdf],
        verbose_name='Copia PDF del Revisado'
    )
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')

    class Meta:
        verbose_name = 'Copia de Revisado Vehicular'
        verbose_name_plural = 'Copias de Revisados Vehiculares'

    def __str__(self):
        return f'Copia del revisado para {self.revisado.vehiculo.placa} ({self.revisado.fecha_emision})'
    
class CopiaPoliza(models.Model):
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE, related_name='copias_documento')
    archivo_pdf = models.FileField(
        upload_to='guantera/polizas/',
        validators=[validate_pdf],
        verbose_name='Copia PDF de la Póliza'
    )
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')

    class Meta:
        verbose_name = 'Copia de Póliza'
        verbose_name_plural = 'Copias de Pólizas'

    def __str__(self):
        return f'Copia de la póliza {self.poliza.numero_poliza}'


class CopiaTarjetaPesosDimensiones(models.Model):
    tarjeta = models.ForeignKey(TarjetaPesosDimensiones, on_delete=models.CASCADE, related_name='copias_documento')
    archivo_pdf = models.FileField(
        upload_to='guantera/pesos_dimensiones/',
        validators=[validate_pdf],
        verbose_name='Copia PDF de la Tarjeta'
    )
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')

    class Meta:
        verbose_name = 'Copia de Tarjeta de Pesos y Dimensiones'
        verbose_name_plural = 'Copias de Tarjetas de Pesos y Dimensiones'

    def __str__(self):
        return f'Copia del permiso {self.tarjeta.numero_permiso}'
    

class StickerPlaca(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='stickers_placa')
    año = models.PositiveIntegerField(verbose_name='Año del Sticker')
    archivo_pdf = models.FileField(
        upload_to='guantera/stickers_placa/',
        validators=[validate_pdf],
        verbose_name='Copia PDF del Sticker'
    )
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')
    
    class Meta:
        verbose_name = 'Sticker de Placa'
        verbose_name_plural = 'Stickers de Placa'
        unique_together = ('vehiculo', 'año')
        ordering = ['-año']

    def __str__(self):
        return f'Sticker {self.año} para {self.vehiculo.placa}'

class ReciboPagoPlaca(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='recibos_placa')
    periodo = models.CharField(max_length=20, verbose_name='Periodo de Pago (e.g., 2025)')
    fecha_pago = models.DateField(verbose_name='Fecha de Pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Pagado')
    archivo_pdf = models.FileField(
        upload_to='guantera/recibos_placa/',
        validators=[validate_pdf],
        verbose_name='Copia PDF del Recibo'
    )
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')

    class Meta:
        verbose_name = 'Recibo de Pago de Placa'
        verbose_name_plural = 'Recibos de Pago de Placa'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'Recibo de placa para {self.vehiculo.placa} - Periodo {self.periodo}'