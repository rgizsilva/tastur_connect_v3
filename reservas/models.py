from django.db import models
from clientes.models import Cliente
from parceiros.models import Parceiro
import uuid
from django.utils import timezone


STATUS_CHOICES = [
    ('confirmada', 'Confirmada'),
    ('pendente', 'Pendente'),
    ('cancelada', 'Cancelada'),
    ('concluida', 'Concluída'),
]

TIPO_PACOTE_CHOICES = [
    ('nacional', 'Nacional'),
    ('internacional', 'Internacional'),
    ('cruzeiro', 'Cruzeiro'),
    ('corporativo', 'Corporativo'),
]

CANAL_VENDA_CHOICES = [
    ('presencial', 'Presencial'),
    ('telefone', 'Telefone'),
    ('site', 'Site'),
    ('whatsapp', 'WhatsApp'),
    ('indicacao', 'Indicação'),
]


class Reserva(models.Model):
    numero_reserva = models.CharField(max_length=10, primary_key=True, default=uuid.uuid4().hex[:10])
    nome_cliente = models.CharField(max_length=100)
    data_entrada = models.DateField(default=timezone.now)
    cpf_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    colaborador_responsavel = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.ForeignKey(Parceiro, null=False, on_delete=models.CASCADE, related_name='reservas')
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    data_ida = models.DateField()
    data_volta = models.DateField()
    comentarios_adicionais = models.TextField(blank=True, null=True)

    # --- Campos novos para análise no Metabase ---
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pendente', verbose_name='Status da Reserva'
    )
    tipo_pacote = models.CharField(
        max_length=20, choices=TIPO_PACOTE_CHOICES,
        default='nacional', verbose_name='Tipo de Pacote'
    )
    canal_venda = models.CharField(
        max_length=20, choices=CANAL_VENDA_CHOICES,
        default='presencial', verbose_name='Canal de Venda'
    )
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True, verbose_name='Valor Total (R$)'
    )
    numero_passageiros = models.PositiveIntegerField(
        default=1, verbose_name='Nº de Passageiros'
    )
    avaliacao_cliente = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='Avaliação do Cliente (1-5)'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def duracao_viagem(self):
        """Retorna o número de dias da viagem."""
        if self.data_ida and self.data_volta:
            return (self.data_volta - self.data_ida).days
        return None

    def __str__(self):
        return f"Reserva {self.numero_reserva} - {self.nome_cliente}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
