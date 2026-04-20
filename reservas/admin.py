from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('numero_reserva', 'nome_cliente', 'destino', 'data_ida', 'data_volta',
                    'status', 'tipo_pacote', 'canal_venda', 'valor_total', 'colaborador_responsavel')
    list_filter = ('status', 'tipo_pacote', 'canal_venda', 'data_ida')
    search_fields = ('nome_cliente', 'destino', 'origem', 'colaborador_responsavel')
    list_editable = ('status',)
    date_hierarchy = 'data_ida'
    fieldsets = (
        ('Dados Principais', {
            'fields': ('numero_reserva', 'nome_cliente', 'cpf_cliente', 'colaborador_responsavel')
        }),
        ('Destino e Datas', {
            'fields': ('origem', 'destino', 'data_entrada', 'data_ida', 'data_volta')
        }),
        ('Parceiro', {
            'fields': ('nome_fantasia', 'cnpj')
        }),
        ('Detalhes Comerciais', {
            'fields': ('status', 'tipo_pacote', 'canal_venda', 'valor_total', 'numero_passageiros', 'avaliacao_cliente')
        }),
        ('Observações', {
            'fields': ('comentarios_adicionais',),
            'classes': ('collapse',)
        }),
    )
