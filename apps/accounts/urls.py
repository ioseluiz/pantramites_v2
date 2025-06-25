from django.urls import path
from .views import (SignUpView,
                    CustomLoginView, 
                    CustomLogoutView, 
                    HomePageView, 
                    ProfileUpdateView, 
                    EmpresaCreateView,
                    load_corregimientos,
                    load_distritos)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # Django espera que las URLs de login y logout se llamen así por defecto
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('empresas/nueva/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('ajax/load-distritos/', load_distritos, name='ajax_load_distritos'),
    path('ajax/load-corregimientos/', load_corregimientos, name='ajax_load_corregimientos'),
    path('', HomePageView.as_view(), name='home'),
]