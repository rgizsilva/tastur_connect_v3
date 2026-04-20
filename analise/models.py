from django.db import models

class AnaliseDados(models.Model):
    pacotes_vendidos = models.IntegerField(default=0, verbose_name="Quantidade de Pacotes Vendidos")
    idade_media_clientes = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Idade Média dos Clientes")
    valor_medio_pacotes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Médio dos Pacotes")
    valor_minimo_pacote = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Mínimo do Pacote")
    valor_maximo_pacote = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Máximo do Pacote")
    data_analise = models.DateTimeField(auto_now_add=True, verbose_name="Data da Análise")

    class Meta:
        verbose_name = "Análise de Dados"
        verbose_name_plural = "Análises de Dados"
        unique_together = ('id',) 

    def __str__(self):
        return f"Análise de Dados de {self.data_analise.strftime('%d/%m/%Y %H:%M')}"
