from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/colaborador/', views.login_colaborador, name='login_colaborador'),
    path('login/cliente/', views.login_cliente, name='login_cliente'),
    path('logout/', views.logout_view, name='logout'),
    path('selecao/colaborador/', views.selecao_colaborador, name='selecao_colaborador'),
    path('selecao/cliente/', views.selecao_cliente, name='selecao_cliente'),
    path('colaborador/cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cliente/reservas/', views.consultar_reserva_cliente, name='consultar_reserva_cliente'),
    path('reservas/pdf/<str:numero_reserva>/', views.gerar_pdf_reserva, name='gerar_pdf_reserva'),
]

