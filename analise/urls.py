# analise/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnaliseDadosViewSet, relatorio_analise, dashboard_page

app_name = 'analise'

router = DefaultRouter()
router.register(r'dados', AnaliseDadosViewSet, basename='analise-dados')

urlpatterns = [
    path('relatorio/', relatorio_analise, name='relatorio'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('', include(router.urls)),
]