from django.db import models
from django.contrib.auth.models import User

class Colaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.nome_completo

from decimal import Decimal
from datetime import datetime

class AnaliseDados(models.Model):
    total_reservas = models.IntegerField()
    media_valor_reservas = models.DecimalField(max_digits=10, decimal_places=2)
    total_clientes = models.IntegerField()
    media_idade_clientes = models.IntegerField()
    data_analise = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análise de Dados - {self.data_analise.strftime('%Y-%m-%d %H:%M')}"

# Dados simulados para popular a tabela
def popular_analise_dados():
    if AnaliseDados.objects.count() == 0:
        AnaliseDados.objects.create(
            total_reservas=150,
            media_valor_reservas=Decimal('250.75'),
            total_clientes=85,
            media_idade_clientes=32,
            data_analise=datetime.now()
        )
        AnaliseDados.objects.create(
            total_reservas=160,
            media_valor_reservas=Decimal('265.50'),
            total_clientes=90,
            media_idade_clientes=33,
            data_analise=datetime.now()
        )
        print("Tabela AnaliseDados populada com dados simulados.")
    else:
        print("Tabela AnaliseDados já contém dados.")

# Esta função deve ser chamada em um management command ou no AppConfig.ready()
# Para fins de simulação e teste, vou apenas defini-la aqui.
# No ambiente real, você precisará garantir que ela seja executada.
# Exemplo de como chamar no shell do Django:
# from seu_app.models import popular_analise_dados
# popular_analise_dados()