from django.contrib import admin
from .models import Colaborador

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'user', 'telefone')
    search_fields = ('nome_completo', 'user__username')
    list_filter = ('user__is_active',)
