from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ColaboradorLoginForm, ClienteLoginForm, ColaboradorForm 
from .models import Colaborador 
from clientes.models import Cliente 
from reservas.models import Reserva 
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
import re 


def home(request):
    """Página inicial do sistema Tastur Connect"""
    return render(request, 'core/home.html')


def login_colaborador(request):
    """Página de login para colaboradores"""
    if request.method == 'POST':
        form = ColaboradorLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.first_name or username}!')
                return redirect('core:selecao_colaborador')
            else:
                messages.error(request, 'Usuário ou senha inválidos')
        else:
            messages.error(request, 'Erro no formulário')
    else:
        form = ColaboradorLoginForm()
    return render(request, 'core/login_colaborador.html', {'form': form})


def login_cliente(request):
    """Página de login para clientes"""
    if request.method == 'POST':
        form = ClienteLoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data.get('cpf')
            senha = form.cleaned_data.get('senha')
            try:
                cliente = Cliente.objects.get(cpf_cliente=cpf)
                
                if cliente.senha == senha:
                    request.session['cliente_cpf'] = cpf
                    request.session['cliente_nome'] = cliente.nome_completo
                    messages.success(request, f'Bem-vindo, {cliente.nome_completo}!')
                    return redirect('core:selecao_cliente')
                else:
                    messages.error(request, 'Senha incorreta')
            except Cliente.DoesNotExist:
                messages.error(request, 'CPF não encontrado')
        else:
            messages.error(request, 'Erro no formulário')
    else:
        form = ClienteLoginForm()
    return render(request, 'core/login_cliente.html', {'form': form})


def logout_view(request):
    """Função para realizar logout para colaboradores e clientes"""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Usuário {username} desconectado com sucesso!')
    elif 'cliente_cpf' in request.session:
        cliente_nome = request.session.pop('cliente_nome', 'Cliente')
        request.session.pop('cliente_cpf', None)
        messages.success(request, f'{cliente_nome} desconectado com sucesso!')
    return redirect('core:home')


@login_required
def selecao_colaborador(request):
    """Página de seleção de opções para colaboradores logados"""
    return render(request, 'core/selecao_colaborador.html')


def selecao_cliente(request):
    """Página de seleção de opções para clientes logados"""
    if 'cliente_cpf' not in request.session:
        messages.error(request, 'Você precisa fazer login para acessar esta página')
        return redirect('core:login_cliente')
    return render(request, 'core/selecao_cliente.html')


@login_required
def cadastrar_colaborador(request):
    """Cadastro de novos colaboradores (somente para superusuários)"""
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página')
        return redirect('core:selecao_colaborador')

    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            Colaborador.objects.create(
                user=user,
                nome_completo=form.cleaned_data['nome_completo'],
                telefone=form.cleaned_data['telefone']
            )

            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('core:selecao_colaborador')
    else:
        form = ColaboradorForm()

    return render(request, 'core/cadastrar_colaborador.html', {'form': form})

def consultar_reserva_cliente(request):
    """Página de consulta de reservas do cliente"""
    if 'cliente_cpf' not in request.session:
        messages.error(request, 'Você precisa fazer login para acessar esta página')
        return redirect('core:login_cliente')

    cpf_session = request.session['cliente_cpf'] 
    reservas = Reserva.objects.filter(cpf_cliente__cpf_cliente=cpf_session)

    if not reservas.exists():
        messages.info(request, 'Você não possui reservas registradas.')

    return render(request, 'core/consultar_reserva_cliente.html', {
        'reservas': reservas,
    })

def gerar_pdf_reserva(request, numero_reserva):
    """Gera o PDF para a reserva do cliente usando numero_reserva."""
    try:
        reserva = Reserva.objects.get(numero_reserva=numero_reserva)
    except Reserva.DoesNotExist:
        messages.error(request, 'Reserva não encontrada.')
        return redirect('core:home') 

    cpf_bruto = reserva.cpf_cliente.cpf_cliente if hasattr(reserva.cpf_cliente, 'cpf_cliente') else str(reserva.cpf_cliente)
    cleaned_cpf = re.sub(r'\D', '', cpf_bruto)
    if len(cleaned_cpf) != 11:
        cleaned_cpf = cpf_bruto

    context = {
        'reserva': reserva,
        'cleaned_cpf': cleaned_cpf
    }
    html_string = render_to_string('core/consultar_reserva_cliente_pdf.html', context)
    
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="voucher_reserva_{reserva.numero_reserva}.pdf"'
    
    return response

