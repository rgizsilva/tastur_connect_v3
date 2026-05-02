from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('consultar/', views.consultar_reserva, name='consultar_reserva'),
    path('cadastrar/', views.cadastrar_reserva, name='cadastrar_reserva'),
    path('sucesso/<str:numero_reserva>/', views.sucesso_reserva, name='sucesso_reserva'),
    path('editar/<str:numero_reserva>/', views.editar_reserva, name='editar_reserva'),
    path('excluir/<str:numero_reserva>/', views.excluir_reserva, name='excluir_reserva'),
]