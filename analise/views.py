# analise/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Min, Max, Count, Sum
from django.utils import timezone
from django.shortcuts import render

from .models import AnaliseDados
from .serializers import AnaliseDadosSerializer


def dashboard_page(request):
        return render(request, 'analise/dashboard.html')
class AnaliseDadosViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint para análise de dados do sistema Tastur Connect.

    GET  /api/analise/dados/          -> Retorna a análise mais recente salva.
    POST /api/analise/dados/atualizar/ -> Calcula e salva nova análise com dados REAIS do banco.
    GET  /api/analise/dados/resumo/   -> Retorna resumo ao vivo sem salvar (dados reais).
    """

    queryset = AnaliseDados.objects.all()
    serializer_class = AnaliseDadosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """GET: retorna apenas o registro mais recente."""
        latest = AnaliseDados.objects.order_by('-data_analise').first()
        if latest:
            return [latest]
        return AnaliseDados.objects.none()
    

    @action(detail=False, methods=['post'])
    def atualizar(self, request):
        """
        POST: calcula métricas reais das tabelas de Reservas e Clientes
        e persiste um novo registro de AnaliseDados.
        """
        try:
            from reservas.models import Reserva
            from clientes.models import Cliente
            from django.db.models.functions import ExtractYear
            from datetime import date

            # --- Métricas de reservas ---
            reservas_qs = Reserva.objects.all()
            total_reservas = reservas_qs.count()

            valor_stats = reservas_qs.filter(
                valor_total__isnull=False
            ).aggregate(
                media=Avg('valor_total'),
                minimo=Min('valor_total'),
                maximo=Max('valor_total'),
                total_faturado=Sum('valor_total'),
            )

            # --- Idade média dos clientes ---
            hoje = date.today()
            clientes = Cliente.objects.all()
            idades = []
            for c in clientes:
                if c.data_nascimento:
                    idade = (hoje - c.data_nascimento).days // 365
                    idades.append(idade)
            idade_media = (sum(idades) / len(idades)) if idades else 0.0

            novo = AnaliseDados.objects.create(
                pacotes_vendidos=total_reservas,
                idade_media_clientes=round(idade_media, 2),
                valor_medio_pacotes=valor_stats['media'] or 0,
                valor_minimo_pacote=valor_stats['minimo'] or 0,
                valor_maximo_pacote=valor_stats['maximo'] or 0,
            )
            serializer = self.get_serializer(novo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Falha ao gerar análise: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def resumo(self, request):
        """
        GET: retorna um resumo ao vivo dos dados reais sem persistir no banco.
        Ideal para dashboards em tempo real.
        """
        try:
            from reservas.models import Reserva
            from clientes.models import Cliente
            from datetime import date

            reservas_qs = Reserva.objects.all()
            total = reservas_qs.count()

            por_status = {
                item['status']: item['total']
                for item in reservas_qs.values('status').annotate(total=Count('status'))
            }
            por_tipo = {
                item['tipo_pacote']: item['total']
                for item in reservas_qs.values('tipo_pacote').annotate(total=Count('tipo_pacote'))
            }
            por_canal = {
                item['canal_venda']: item['total']
                for item in reservas_qs.values('canal_venda').annotate(total=Count('canal_venda'))
            }

            valor_stats = reservas_qs.filter(valor_total__isnull=False).aggregate(
                media=Avg('valor_total'),
                minimo=Min('valor_total'),
                maximo=Max('valor_total'),
                total_faturado=Sum('valor_total'),
            )

            hoje = date.today()
            idades = [
                (hoje - c.data_nascimento).days // 365
                for c in Cliente.objects.all() if c.data_nascimento
            ]
            idade_media = round(sum(idades) / len(idades), 1) if idades else 0

            return Response({
                "total_reservas": total,
                "total_clientes": Cliente.objects.count(),
                "idade_media_clientes": idade_media,
                "valor_medio": float(valor_stats['media'] or 0),
                "valor_minimo": float(valor_stats['minimo'] or 0),
                "valor_maximo": float(valor_stats['maximo'] or 0),
                "total_faturado": float(valor_stats['total_faturado'] or 0),
                "por_status": por_status,
                "por_tipo_pacote": por_tipo,
                "por_canal_venda": por_canal,
                "gerado_em": timezone.now().isoformat(),
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@login_required
def relatorio_analise(request):
    """View HTML com relatório completo de análise."""
    from reservas.models import Reserva
    from clientes.models import Cliente
    from django.db.models import Count, Sum, Avg
    from datetime import date

    reservas_qs = Reserva.objects.all()
    total_reservas = reservas_qs.count()
    total_clientes = Cliente.objects.count()

    valor_stats = reservas_qs.filter(valor_total__isnull=False).aggregate(
        media=Avg('valor_total'),
        minimo=Min('valor_total'),
        maximo=Max('valor_total'),
        total_faturado=Sum('valor_total'),
    )

    hoje = date.today()
    idades = [
        (hoje - c.data_nascimento).days // 365
        for c in Cliente.objects.all() if c.data_nascimento
    ]
    idade_media = round(sum(idades) / len(idades), 1) if idades else 0

    por_status = list(reservas_qs.values('status').annotate(total=Count('status')).order_by('-total'))
    por_tipo   = list(reservas_qs.values('tipo_pacote').annotate(total=Count('tipo_pacote')).order_by('-total'))
    por_canal  = list(reservas_qs.values('canal_venda').annotate(total=Count('canal_venda')).order_by('-total'))

    # Top 5 destinos
    top_destinos = list(
        reservas_qs.values('destino').annotate(total=Count('destino')).order_by('-total')[:5]
    )

    # Última análise salva
    try:
        ultima_analise = AnaliseDados.objects.latest('data_analise')
    except AnaliseDados.DoesNotExist:
        ultima_analise = None

    context = {
        'total_reservas': total_reservas,
        'total_clientes': total_clientes,
        'idade_media': idade_media,
        'valor_stats': valor_stats,
        'por_status': por_status,
        'por_tipo': por_tipo,
        'por_canal': por_canal,
        'top_destinos': top_destinos,
        'ultima_analise': ultima_analise,
    }
    return render(request, 'analise/relatorio_analise.html', context)
