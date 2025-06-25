from django.urls import path
from .views import (VehiculoListView,
                     VehiculoDetailView,
                       VehiculoCreateView,
                       load_modelos
                       )

app_name = 'gestion_flota'

urlpatterns = [
    path('flota/', VehiculoListView.as_view(), name='vehiculo_list'),
    path('flota/vehiculo/nuevo/', VehiculoCreateView.as_view(), name='vehiculo_create'),
    path('flota/vehiculo/<int:pk>/', VehiculoDetailView.as_view(), name='vehiculo_detail'),
    path('ajax/load-modelos/', load_modelos, name='ajax_load_modelos'),
]