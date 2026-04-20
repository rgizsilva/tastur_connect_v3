from django.urls import path, re_path
from . import views
app_name = 'parceiros'

urlpatterns = [
    path('cadastrar/', views.cadastrar_parceiro, name='cadastrar_parceiro'),
    path('consultar/', views.consultar_parceiro, name='consultar_parceiro'),
    re_path(r'^parceiros/editar/(?P<cnpj>[\d\.\/-]+)/$', views.editar_parceiro, name='editar_parceiro'),
    re_path(r'^parceiros/excluir/(?P<cnpj>[\d\.\/-]+)/$', views.excluir_parceiro, name='excluir_parceiro'),
]