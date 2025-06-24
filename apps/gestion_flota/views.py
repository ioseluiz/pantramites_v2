from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Vehiculo
from apps.guantera.models import FotoVehiculo, RegistroUnicoVehicular, CopiaPoliza, CopiaRevisadoVehicular, CopiaTarjetaPesosDimensiones, StickerPlaca, ReciboPagoPlaca
from .forms import VehiculoForm
from django.urls import reverse_lazy

class VehiculoListView(LoginRequiredMixin, ListView):
    model = Vehiculo
    template_name = 'gestion_flota/vehiculo_list.html'
    context_object_name = 'vehiculos'
    paginate_by = 12 # Muestra 12 vehículos por página

    def get_queryset(self):
        """
        Esta función asegura que los usuarios solo vean los vehículos
        asociados a su propia empresa.
        """
        user = self.request.user
        if hasattr(user, 'empresa') and user.empresa is not None:
            # Filtra vehículos cuyo propietario pertenezca a la misma empresa que el usuario logueado.
            return Vehiculo.objects.filter(propietario__empresa=user.empresa)
        
        # Si el usuario no tiene una empresa, no ve ningún vehículo.
        return Vehiculo.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa'] = self.request.user.empresa
        return context
    
class VehiculoCreateView(LoginRequiredMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'gestion_flota/vehiculo_form.html'
    success_url = reverse_lazy('gestion_flota:vehiculo_list')

    def get_form_kwargs(self):
        """Pasa el usuario actual al formulario."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Asigna el usuario actual como propietario del vehículo antes de guardarlo.
        """
        form.instance.propietario = self.request.user
        self.object = form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Registrar Nuevo Vehículo"
        return context



class VehiculoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vehiculo
    template_name = 'gestion_flota/vehiculo_detail.html'
    context_object_name = 'vehiculo'

    def test_func(self):
        """
        Esta prueba de seguridad confirma que un usuario solo puede ver
        detalles de un vehículo si este pertenece a su empresa.
        """
        vehiculo = self.get_object()
        user = self.request.user
        if hasattr(user, 'empresa') and user.empresa is not None:
            # Verifica que el vehículo tenga un propietario y que la empresa del propietario coincida.
            return vehiculo.propietario and vehiculo.propietario.empresa == user.empresa
        return False
        
    def get_context_data(self, **kwargs):
        """
        Añade todos los documentos de la guantera al contexto para ser
        mostrados en la plantilla.
        """
        context = super().get_context_data(**kwargs)
        vehiculo = self.get_object()
        context['fotos'] = FotoVehiculo.objects.filter(vehiculo=vehiculo)
        try:
            context['registro_unico'] = RegistroUnicoVehicular.objects.get(vehiculo=vehiculo)
        except RegistroUnicoVehicular.DoesNotExist:
            context['registro_unico'] = None
        # Añadir el resto de documentos de la guantera
        # ...
        return context
