from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django import forms

class CustomUserCreationForm(UserCreationForm):
    """
    Un formulario para crear nuevos usuarios sin privilegios de administrador.
    Hereda de UserCreationForm y especifica el modelo CustomUser.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    """
    Un formulario para actualizar la información de un usuario existente.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

class ProfileUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar los datos del perfil de un usuario.
    """
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'birth_date')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
