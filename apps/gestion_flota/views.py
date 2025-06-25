from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages # Importar el framework de mensajes
from .models import Vehiculo, Modelo
from .forms import VehiculoForm
from apps.guantera.models import FotoVehiculo, RegistroUnicoVehicular

class VehiculoListView(LoginRequiredMixin, ListView):
    model = Vehiculo
    template_name = 'gestion_flota/vehiculo_list.html'
    context_object_name = 'vehiculos'
    paginate_by = 12

    def get_queryset(self):
        """
        Esta función asegura que los usuarios solo vean los vehículos
        asociados a su propia empresa, ordenando por los más recientes primero.
        """
        user = self.request.user
        # Se verifica que el usuario esté autenticado y tenga una empresa asociada
        if user.is_authenticated and hasattr(user, 'empresa') and user.empresa is not None:
            return Vehiculo.objects.filter(propietario__empresa=user.empresa).order_by('-id')
        
        return Vehiculo.objects.none()

    def get_context_data(self, **kwargs):
        """
        Añade la empresa del usuario al contexto para mostrarla en la plantilla.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Nos aseguramos de pasar la empresa al contexto solo si existe.
        if user.is_authenticated and hasattr(user, 'empresa') and user.empresa is not None:
            context['empresa'] = user.empresa
        else:
            context['empresa'] = None
        return context

class VehiculoCreateView(LoginRequiredMixin, CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'gestion_flota/vehiculo_form.html'
    success_url = reverse_lazy('gestion_flota:vehiculo_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Asigna el usuario actual como propietario y añade un mensaje de éxito.
        """
        form.instance.propietario = self.request.user
        messages.success(self.request, f'¡El vehículo con placa "{form.cleaned_data["placa"]}" ha sido registrado exitosamente!')
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
        vehiculo = self.get_object()
        user = self.request.user
        if hasattr(user, 'empresa') and user.empresa is not None:
            return vehiculo.propietario and vehiculo.propietario.empresa == user.empresa
        return False
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculo = self.get_object()
        context['fotos'] = FotoVehiculo.objects.filter(vehiculo=vehiculo)
        try:
            context['registro_unico'] = RegistroUnicoVehicular.objects.get(vehiculo=vehiculo)
        except RegistroUnicoVehicular.DoesNotExist:
            context['registro_unico'] = None
        return context

def load_modelos(request):
    marca_id = request.GET.get('marca_id')
    modelos = Modelo.objects.filter(marca_id=marca_id).order_by('nombre')
    return JsonResponse(list(modelos.values('id', 'nombre')), safe=False)
