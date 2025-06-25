from django import forms
from .models import Vehiculo, Marca, Modelo, Municipio

class VehiculoForm(forms.ModelForm):
    """
    Formulario para la creación y edición de vehículos, con desplegables
    dependientes para Marca y Modelo, actualizado a la nueva estructura.
    """
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all().order_by('nombre'),
        label="Marca",
        required=True
    )

    class Meta:
        model = Vehiculo
        fields = [
            'placa', 'marca', 'modelo', 'municipio_placa', 'is_carga',
            'acreedor_hipotecario', 'ano_fabricacion', 'numero_motor', 'color',
            'tipo_combustible', 'mes_renovacion_placa'
        ]
        widgets = {
            'ano_fabricacion': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
        }

    def __init__(self, *args, **kwargs):
        # **LA CORRECCIÓN ESTÁ AQUÍ**
        # Se extrae el argumento 'user' de kwargs antes de llamar al constructor padre.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['modelo'].queryset = Modelo.objects.none()

        # Añadir clases de Tailwind a los campos del formulario
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all'

        if 'marca' in self.data:
            try:
                marca_id = int(self.data.get('marca'))
                self.fields['modelo'].queryset = Modelo.objects.filter(marca_id=marca_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.modelo:
            self.fields['marca'].initial = self.instance.modelo.marca
            self.fields['modelo'].queryset = Modelo.objects.filter(marca=self.instance.modelo.marca).order_by('nombre')
