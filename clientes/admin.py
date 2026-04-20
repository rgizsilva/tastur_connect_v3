from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf_cliente', 'nome_completo', 'telefone', 'cidade', 'possui_reserva')
    search_fields = ('cpf_cliente', 'nome_completo')
    list_filter = ('cidade', 'uf', 'possui_reserva')
    fieldsets = (
        (None, {
            'fields': ('cpf_cliente', 'nome_completo', 'data_nascimento')
        }),
        ('Informações de Contato', {
            'fields': ('telefone', 'celular')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'complemento', 'cep', 'cidade', 'uf')
        }),
        ('Acesso ao Sistema', {
            'fields': ('senha',),
            'description': 'Defina uma senha para o cliente acessar o sistema usando o CPF como login.'
        }),
        ('Status', {
            'fields': ('possui_reserva',)
        }),
    )
