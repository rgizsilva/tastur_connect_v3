# Generated manually - novos campos para análise no Metabase
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0005_alter_reserva_numero_reserva'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='status',
            field=models.CharField(
                choices=[
                    ('confirmada', 'Confirmada'),
                    ('pendente', 'Pendente'),
                    ('cancelada', 'Cancelada'),
                    ('concluida', 'Concluída'),
                ],
                default='pendente',
                max_length=20,
                verbose_name='Status da Reserva',
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='tipo_pacote',
            field=models.CharField(
                choices=[
                    ('nacional', 'Nacional'),
                    ('internacional', 'Internacional'),
                    ('cruzeiro', 'Cruzeiro'),
                    ('corporativo', 'Corporativo'),
                ],
                default='nacional',
                max_length=20,
                verbose_name='Tipo de Pacote',
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='canal_venda',
            field=models.CharField(
                choices=[
                    ('presencial', 'Presencial'),
                    ('telefone', 'Telefone'),
                    ('site', 'Site'),
                    ('whatsapp', 'WhatsApp'),
                    ('indicacao', 'Indicação'),
                ],
                default='presencial',
                max_length=20,
                verbose_name='Canal de Venda',
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='valor_total',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name='Valor Total (R$)',
            ),
        ),
        migrations.AddField(
            model_name='reserva',
            name='numero_passageiros',
            field=models.PositiveIntegerField(default=1, verbose_name='Nº de Passageiros'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='avaliacao_cliente',
            field=models.PositiveSmallIntegerField(
                blank=True,
                null=True,
                verbose_name='Avaliação do Cliente (1-5)',
            ),
        ),
    ]
