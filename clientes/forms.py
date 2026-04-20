from django import forms
from .models import Cliente
import re
from datetime import datetime

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo',
                'aria-label': 'Nome completo do cliente'
            }),
            'cpf_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'aria-label': 'CPF do cliente'
            }),
            'data_nascimento': forms.TextInput(attrs={
                'class': 'form-control datepicker-br',
                'placeholder': 'DD/MM/AAAA',
                'aria-label': 'Data de nascimento no formato dia, mês e ano'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com',
                'aria-label': 'Endereço de e-mail do cliente'
            }),
        }

    def clean_data_nascimento(self):
        data = self.cleaned_data.get('data_nascimento')
        if data and isinstance(data, str):
            try:
                return datetime.strptime(data, '%d/%m/%Y').date()
            except ValueError:
                raise forms.ValidationError('Data inválida. Use o formato DD/MM/AAAA.')
        return data

    def clean_cpf_cliente(self):
        cpf = self.cleaned_data.get('cpf_cliente')
        if cpf:
            cpf_sem_mascara = re.sub(r'\D', '', cpf)
            return cpf_sem_mascara
        return cpf


class ConsultaClienteForm(forms.Form):
    cpf = forms.CharField(
        max_length=14,
        required=False,
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o CPF do cliente',
            'aria-label': 'Campo para consulta de CPF',
        })
    )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf_sem_mascara = re.sub(r'\D', '', cpf)
            return cpf_sem_mascara
        return cpf