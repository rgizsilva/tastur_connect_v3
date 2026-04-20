from django import forms
from .models import Parceiro

class ParceiroForm(forms.ModelForm):
    class Meta:
        model = Parceiro
        fields = '__all__'
        widgets = {
            'data_entrada': forms.TextInput(
                attrs={
                    'class': 'form-control datepicker-br',
                    'placeholder': 'DD/MM/AAAA'
                }
            ),
        }

class ConsultaParceiroForm(forms.Form):
    cnpj = forms.CharField(max_length=18, required=False, label='CNPJ')
