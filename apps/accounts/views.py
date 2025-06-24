from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile

class SignUpView(CreateView):
    """
    Vista para el registro de nuevos usuarios.
    Utiliza nuestro formulario personalizado y redirige al login al tener éxito.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    """
    Vista para el inicio de sesión de usuarios.
    Django provee la mayor parte de la lógica. Solo especificamos la plantilla.
    """
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    """
    Vista para el cierre de sesión.
    """
    pass

class HomePageView(TemplateView):
    """
    Una vista simple para la página de inicio.
    """
    template_name = 'home.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para que un usuario vea y actualice su perfil.
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Devuelve el perfil del usuario actualmente logueado
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Mi Perfil"
        return context
