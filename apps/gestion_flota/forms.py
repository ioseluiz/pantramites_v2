from django import forms
from .models import Vehiculo, Modelo, Municipio

class VehiculoForm(forms.ModelForm):
    """
    Formulario para la creación y edición de vehículos por parte de los usuarios.
    """
    class Meta:
        model = Vehiculo
        fields = [
            'placa', 'modelo', 'municipio_placa', 'is_carga', 
            'acreedor_hipotecario', 'ano_fabricacion', 'numero_motor', 'color', 
            'tipo_combustible'
        ]
        widgets = {
            'ano_fabricacion': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
        }

    def __init__(self, *args, **kwargs):
        # El usuario se pasa desde la vista para filtrar los querysets si es necesario
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Opcional: Podrías filtrar los modelos o municipios si tuvieran
        # alguna relación con la empresa del usuario.
        self.fields['modelo'].queryset = Modelo.objects.all().order_by('marca__nombre', 'nombre')
        self.fields['municipio_placa'].queryset = Municipio.objects.all().order_by('provincia__nombre', 'nombre')
        
        # Añadir clases de Tailwind a los campos del formulario
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all'
