from django.contrib import admin
from .models import Parceiro

@admin.register(Parceiro)
class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('cnpj', 'nome_fantasia', 'telefone', 'cidade', 'email')
    search_fields = ('cnpj', 'nome_fantasia', 'email')
    list_filter = ('cidade', 'uf')
