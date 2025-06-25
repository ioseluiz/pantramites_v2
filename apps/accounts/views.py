from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm, EmpresaForm
from .models import Profile
from apps.gestion_flota.models import Corregimiento, Municipio

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Añade un mensaje de éxito que se mostrará en la página de login
        messages.success(self.request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    pass

class HomePageView(TemplateView):
    template_name = 'home.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Mi Perfil"
        return context

class EmpresaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = EmpresaForm
    template_name = 'accounts/empresa_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        # Añadir un mensaje de éxito que se mostrará en la siguiente página
        messages.success(self.request, f'¡La empresa "{form.cleaned_data["nombre"]}" ha sido registrada exitosamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Registrar Nueva Empresa"
        return context

def load_distritos(request):
    provincia_id = request.GET.get('provincia_id')
    distritos = Municipio.objects.filter(provincia_id=provincia_id).order_by('nombre')
    return JsonResponse(list(distritos.values('id', 'nombre')), safe=False)
    
def load_corregimientos(request):
    """
    Carga los corregimientos correspondientes a un distrito (municipio)
    para el desplegable dinámico del formulario.
    """
    # 1. Obtiene el ID del distrito desde la URL (ej: ?distrito_id=5)
    distrito_id = request.GET.get('distrito_id')
    
    # 2. Filtra la base de datos para encontrar todos los corregimientos
    #    que pertenecen a ese distrito.
    corregimientos = Corregimiento.objects.filter(municipio_id=distrito_id).order_by('nombre')
    
    # 3. Convierte el resultado en un formato JSON que JavaScript pueda entender.
    #    Crea una lista de diccionarios, cada uno con el 'id' y 'nombre' del corregimiento.
    return JsonResponse(list(corregimientos.values('id', 'nombre')), safe=False)
