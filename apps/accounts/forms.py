from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Empresa, Profile
from apps.gestion_flota.models import Provincia, Municipio, Corregimiento

class EmpresaForm(forms.ModelForm):
    """
    Formulario para la creación y edición de empresas.
    """
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all().order_by('nombre'),
        label="Provincia",
        required=True
    )
    distrito = forms.ModelChoiceField(
        queryset=Municipio.objects.none(),
        label="Distrito",
        required=True
    )
    corregimiento = forms.ModelChoiceField(
        queryset=Corregimiento.objects.none(),
        label="Corregimiento",
        required=False
    )

    class Meta:
        model = Empresa
        fields = [
            'nombre', 'ruc', 'tipo', 'provincia', 'distrito', 'corregimiento', 'calle', 'casa',
            'email_1', 'email_2', 'telefono_1', 'telefono_2', 'url_logo_empresa'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['distrito'].queryset = Municipio.objects.filter(provincia_id=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.distrito:
            self.fields['distrito'].queryset = self.instance.distrito.provincia.municipios.order_by('nombre')

        if 'distrito' in self.data:
            try:
                distrito_id = int(self.data.get('distrito'))
                self.fields['corregimiento'].queryset = Corregimiento.objects.filter(municipio_id=distrito_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.corregimiento:
            self.fields['corregimiento'].queryset = self.instance.corregimiento.municipio.corregimientos.order_by('nombre')


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para crear nuevos usuarios, asegurando que la empresa se guarde.
    """
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=True,
        label="Empresa",
        empty_label="-- Seleccionar una Empresa --"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('empresa', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        # Llama al método save() de la clase padre para crear el usuario
        user = super().save(commit=False)
        # Asigna la empresa seleccionada desde los datos limpios del formulario
        user.empresa = self.cleaned_data['empresa']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('empresa', 'email', 'first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'birth_date')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
