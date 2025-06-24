from django.contrib import admin
from .models import (
    Provincia, Municipio, Corregimiento,
    Marca, Modelo, Vehiculo,
    Aseguradora, Poliza, RevisadoVehicular, TarjetaPesosDimensiones
)

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia',)
    list_filter = ('provincia',)
    search_fields = ('nombre', 'provincia__nombre',)
    ordering = ('provincia', 'nombre',)

@admin.register(Corregimiento)
class CorregimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'municipio',)
    list_filter = ('municipio__provincia', 'municipio',)
    search_fields = ('nombre', 'municipio__nombre',)
    ordering = ('municipio__provincia', 'municipio', 'nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca',)
    list_filter = ('marca',)
    search_fields = ('nombre', 'marca__nombre',)
    ordering = ('marca', 'nombre',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'ano_fabricacion', 'propietario', 'estado_placa')
    list_filter = ('estado_placa', 'is_carga', 'acreedor_hipotecario', 'modelo__marca', 'municipio_placa__provincia')
    search_fields = ('placa', 'numero_motor', 'propietario__email', 'modelo__nombre', 'modelo__marca__nombre')
    raw_id_fields = ('propietario', 'modelo', 'municipio_placa') # Mejora el rendimiento para llaves foráneas con muchos registros
    ordering = ('-ano_fabricacion',)

@admin.register(Aseguradora)
class AseguradoraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono_contacto')
    search_fields = ('nombre',)

@admin.register(Poliza)
class PolizaAdmin(admin.ModelAdmin):
    list_display = ('numero_poliza', 'vehiculo', 'aseguradora', 'fecha_vencimiento', 'estado')
    list_filter = ('estado', 'activa', 'aseguradora')
    search_fields = ('numero_poliza', 'vehiculo__placa')
    raw_id_fields = ('vehiculo', 'aseguradora')
    ordering = ('-fecha_vencimiento',)

@admin.register(RevisadoVehicular)
class RevisadoVehicularAdmin(admin.ModelAdmin):
    list_display = ('numero_documento', 'vehiculo', 'fecha_vencimiento', 'estado')
    list_filter = ('estado', 'aprobado')
    search_fields = ('numero_documento', 'vehiculo__placa', 'taller_certificado')
    raw_id_fields = ('vehiculo',)
    ordering = ('-fecha_vencimiento',)

@admin.register(TarjetaPesosDimensiones)
class TarjetaPesosDimensionesAdmin(admin.ModelAdmin):
    list_display = ('numero_permiso', 'vehiculo', 'fecha_vencimiento', 'estado')
    list_filter = ('estado', 'entidad_emisora')
    search_fields = ('numero_permiso', 'vehiculo__placa')
    raw_id_fields = ('vehiculo',)
    ordering = ('-fecha_vencimiento',)
