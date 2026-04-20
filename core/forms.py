from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ColaboradorLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ClienteLoginForm(forms.Form):
    cpf = forms.CharField(label='CPF', max_length=14, widget=forms.TextInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            return ''.join(filter(str.isdigit, cpf))
        return cpf

class ColaboradorForm(forms.Form):
    username = forms.CharField(label='Nome de usuário', max_length=150)
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    nome_completo = forms.CharField(label='Nome completo', max_length=100)
    telefone = forms.CharField(label='Telefone', max_length=15)
