# arriendos/forms.py
from django import forms
from .models import Arriendo, Pago


class ArriendoForm(forms.ModelForm):
    class Meta:
        model = Arriendo
        fields = ['nombre', 'capital', 'porcentaje', 'mto_interes', 'fecha', 'estado']
        widgets = {
            'porcentaje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: [1.5, 2.0, 2.5]'}),
            'mto_interes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: [100.0, 150.0]'}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha', 'ano', 'mes', 'tipo_pago']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_pago'].empty_label = "Selecciona un tipo de pago"