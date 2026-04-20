from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('consultar/', views.consultar_cliente, name='consultar_cliente'),
    path('editar/<str:cpf>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<str:cpf>/', views.excluir_cliente, name='excluir_cliente'),
]
