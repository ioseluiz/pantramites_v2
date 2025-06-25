from django.urls import path
from .views import RecordatorioListView

app_name = 'recordatorios'

urlpatterns = [
    path('recordatorios/', RecordatorioListView.as_view(), name='recordatorio_list'),
]