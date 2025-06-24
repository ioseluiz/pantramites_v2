from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, HomePageView, ProfileUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # Django espera que las URLs de login y logout se llamen así por defecto
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('', HomePageView.as_view(), name='home'),
]