from django.contrib import admin
from .models import (
    FotoVehiculo,
    RegistroUnicoVehicular,
    CopiaRevisadoVehicular,
    CopiaPoliza,
    CopiaTarjetaPesosDimensiones,
    StickerPlaca,
    ReciboPagoPlaca
)

@admin.register(FotoVehiculo)
class FotoVehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'descripcion', 'fecha_carga')
    list_filter = ('fecha_carga',)
    search_fields = ('vehiculo__placa', 'descripcion')

@admin.register(RegistroUnicoVehicular)
class RegistroUnicoVehicularAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha_emision', 'fecha_carga')
    search_fields = ('vehiculo__placa',)

@admin.register(CopiaRevisadoVehicular)
class CopiaRevisadoVehicularAdmin(admin.ModelAdmin):
    list_display = ('revisado', 'fecha_carga')
    search_fields = ('revisado__vehiculo__placa',)

@admin.register(CopiaPoliza)
class CopiaPolizaAdmin(admin.ModelAdmin):
    list_display = ('poliza', 'fecha_carga')
    search_fields = ('poliza__numero_poliza', 'poliza__vehiculo__placa')

@admin.register(CopiaTarjetaPesosDimensiones)
class CopiaTarjetaPesosDimensionesAdmin(admin.ModelAdmin):
    list_display = ('tarjeta', 'fecha_carga')
    search_fields = ('tarjeta__numero_permiso', 'tarjeta__vehiculo__placa')

@admin.register(StickerPlaca)
class StickerPlacaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'año', 'fecha_carga')
    search_fields = ('vehiculo__placa',)
    list_filter = ('año',)

@admin.register(ReciboPagoPlaca)
class ReciboPagoPlacaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'periodo', 'fecha_pago', 'monto')
    search_fields = ('vehiculo__placa', 'periodo')
    list_filter = ('fecha_pago',)
