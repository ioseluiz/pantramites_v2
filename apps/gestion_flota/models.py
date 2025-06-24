from django.db import models
from django.conf import settings

# -----------------------------------------------------------------------------
# Modelos Geográficos
# -----------------------------------------------------------------------------
class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Provincia')

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
class Municipio(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='municipios')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Municipio')

    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        unique_together = ('provincia', 'nombre')
        ordering = ['provincia', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.provincia.nombre})"
    

class Corregimiento(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='corregimientos')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Corregimiento')
    
    class Meta:
        verbose_name = 'Corregimiento'
        verbose_name_plural = 'Corregimientos'
        unique_together = ('municipio', 'nombre')
    
    def __str__(self):
        return f"{self.nombre}, {self.municipio}"

# -----------------------------------------------------------------------------
# Modelos de Vehículos
# -----------------------------------------------------------------------------

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Marca del Vehiculo')

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
class Modelo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Modelo')

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        unique_together = ('marca', 'nombre')
        ordering = ['marca', 'nombre']

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"
    
class Vehiculo(models.Model):
    TIPO_COMBUSTIBLE = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL','Diesel'),
        ('ELECTRICO', 'Electrico'),
        ('HIBRIDO', 'Hibrido')
    ]
    STATUS_CHOICES = [
        ('VIGENTE', 'Vigente'),
        ('POR_VENCER', 'Por Vencer'),
        ('VENCIDO', 'Vencido'),
    ]
    MESES = [
        ('ENERO', 'Enero'),
        ('FEBRERO', 'Febrero'),
        ('MARZO', 'Marzo'),
        ('ABRIL', 'Abril'),
        ('MAYO', 'Mayo'),
        ('JUNIO', 'Junio'),
        ('JULIO','Julio'),
        ('AGOSTO', 'Agosto'),
        ('SEPTIEMBRE', 'Septiembre'),
        ('OCTUBRE','Octubre'),
        ('NOVIEMBRE','Noviembre'),
        ('DICIEMBRE','Diciembre'),
    ]
    placa = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, related_name='vehiculos')
    acreedor_hipotecario = models.BooleanField(default=False, verbose_name='Tiene acreedor hipotecario')
    municipio_placa = models.ForeignKey(
        Municipio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehiculos_registrados',
        verbose_name='Municipio de la placa'
    )
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehiculos')
    is_carga = models.BooleanField(default=False, verbose_name='Es vehículo de carga')
    ano_fabricacion = models.PositiveBigIntegerField(verbose_name='Ano de Fabricacion')
    numero_motor = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='Numero de Motor')
    color = models.CharField(max_length=30, blank=True)
    tipo_combustible = models.CharField(max_length=20, choices=TIPO_COMBUSTIBLE, default='GASOLINA')
    mes_renovacion_placa = models.CharField(max_length=100, choices=MESES, default='ENERO')
    estado_placa = models.CharField(max_length=20, choices=STATUS_CHOICES, default='VIGENTE', verbose_name='Estado de la Placa')

    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'
        ordering = ['-ano_fabricacion', 'placa']

    def __str__(self):
        return f"{self.modelo} ({self.placa})"
    

# -----------------------------------------------------------------------------
# Modelos de Seguros
# -----------------------------------------------------------------------------
class Aseguradora(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Aseguradora')
    telefono_contacto = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Aseguradora'
        verbose_name_plural = 'Aseguradoras'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Poliza(models.Model):
    STATUS_CHOICES = [
        ('VIGENTE', 'Vigente'),
        ('POR_VENCER', 'Por Vencer'),
        ('VENCIDO', 'Vencido'),
    ]
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, related_name='poliza')
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.PROTECT, related_name='polizas')
    numero_poliza = models.CharField(max_length=50, unique=True, verbose_name='Número de Póliza')
    fecha_emision = models.DateField(verbose_name='Fecha de Inicio')
    fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento')
    activa = models.BooleanField(default=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='VIGENTE', verbose_name='Estado')

    class Meta:
        verbose_name = 'Póliza de Seguro'
        verbose_name_plural = 'Pólizas de Seguro'
        ordering = ['-fecha_vencimiento']

    def __str__(self):
        return f'Póliza {self.numero_poliza} para {self.vehiculo.placa}'
    
class RevisadoVehicular(models.Model):
    STATUS_CHOICES = [
        ('VIGENTE', 'Vigente'),
        ('POR_VENCER', 'Por Vencer'),
        ('VENCIDO', 'Vencido'),
    ]
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='revisados')
    taller_certificado = models.CharField(max_length=200, verbose_name='Taller Certificado')
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name='Número de Documento')
    fecha_emision = models.DateField(verbose_name='Fecha de Emisión')
    fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento')
    aprobado = models.BooleanField(default=True, verbose_name='Aprobado')
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='VIGENTE', verbose_name='Estado')

    class Meta:
        verbose_name = 'Revisado Vehicular'
        verbose_name_plural = 'Revisados Vehiculares'
        ordering = ['-fecha_vencimiento']
        unique_together = ('vehiculo', 'fecha_emision')

    def __str__(self):
        return f'Revisado para {self.vehiculo.placa} - Vence: {self.fecha_vencimiento}'
    
class TarjetaPesosDimensiones(models.Model):
    STATUS_CHOICES = [
        ('VIGENTE', 'Vigente'),
        ('POR_VENCER', 'Por Vencer'),
        ('VENCIDO', 'Vencido'),
    ]
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='tarjetas_pesos_dimensiones')
    numero_permiso = models.CharField(max_length=50, unique=True, verbose_name='Número de Permiso')
    entidad_emisora = models.CharField(max_length=200, verbose_name='Entidad Emisora')
    fecha_emision = models.DateField(verbose_name='Fecha de Emisión')
    fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento')
    peso_maximo_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Peso Máximo Autorizado (kg)')
    dimensiones = models.CharField(max_length=100, blank=True, verbose_name='Dimensiones (Largo x Ancho x Alto)')
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='VIGENTE', verbose_name='Estado')

    class Meta:
        verbose_name = 'Tarjeta de Pesos y Dimensiones'
        verbose_name_plural = 'Tarjetas de Pesos y Dimensiones'
        ordering = ['-fecha_vencimiento']

    def __str__(self):
        return f'Permiso {self.numero_permiso} para {self.vehiculo.placa}'

