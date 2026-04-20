# tests/test_core.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Colaborador
from pyquery import PyQuery as pq 

pytestmark = pytest.mark.django_db


def test_colaborador_model():
    user = User.objects.create_user(username='testuser', password='password123')
    colaborador = Colaborador.objects.create(
        user=user,
        nome_completo='João da Silva',
        telefone='(11) 99999-8888'
    )
    assert str(colaborador) == 'João da Silva'
    assert Colaborador.objects.count() == 1
    assert User.objects.count() == 1


def test_home_view_loads_correctly(client):
    url = reverse('core:home')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Tastur Connect' in response.content


def test_login_colaborador_view_loads_correctly(client):
    """
    Testa se a página de login do colaborador carrega corretamente.
    """
    url = reverse('core:login_colaborador')
    response = client.get(url)
    assert response.status_code == 200

    html = response.content.decode('utf-8')
    doc = pq(html)
    
    assert "Login Colaborador" in doc('h2').text()


def test_login_colaborador_success(client):
    username = 'colaborador_teste'
    password = 'senha_super_segura'
    user = User.objects.create_user(username=username, password=password, first_name='João')
    Colaborador.objects.create(user=user, nome_completo='João Teste', telefone='12345')

    login_url = reverse('core:login_colaborador')
    response = client.post(login_url, {
        'username': username,
        'password': password,
    })

    assert response.status_code == 302
    assert response.url == reverse('core:selecao_colaborador')

    redirect_response = client.get(response.url)
    assert b'Bem-vindo, Jo' in redirect_response.content
