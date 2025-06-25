from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recordatorio

class RecordatorioListView(LoginRequiredMixin, ListView):
    model = Recordatorio
    template_name = 'recordatorios/recordatorio_list.html'
    context_object_name = 'recordatorios'
    paginate_by = 15

    def get_queryset(self):
        # Muestra solo los recordatorios del usuario logueado, los más nuevos primero
        return Recordatorio.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Marcar los recordatorios como leídos al ver la página
        Recordatorio.objects.filter(usuario=self.request.user, leido=False).update(leido=True)
        context['page_title'] = "Mis Recordatorios"
        return context
