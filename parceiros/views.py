from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Parceiro
from .forms import ParceiroForm, ConsultaParceiroForm
import re

@login_required
def cadastrar_parceiro(request):
    """Cadastro de novos parceiros (apenas para colaboradores)"""
    if request.method == 'POST':
        form = ParceiroForm(request.POST)
        if form.is_valid():
            parceiro = form.save()
            messages.success(request, 'Parceiro cadastrado com sucesso!')
            return redirect('parceiros:consultar_parceiro')
        else:
            messages.error(request, 'Erro ao cadastrar parceiro. Verifique os dados informados.')
    else:
        form = ParceiroForm()
    return render(request, 'parceiros/cadastrar_parceiro.html', {'form': form})

@login_required
def consultar_parceiro(request):
    """Consulta de parceiros (apenas para colaboradores)"""
    form = ConsultaParceiroForm(request.GET or None)
    parceiros = []

    if form.is_valid() and request.GET:
        cnpj = form.cleaned_data.get('cnpj')
        if cnpj:
            cnpj_clean = re.sub(r'\D', '', cnpj) 
            parceiros = Parceiro.objects.filter(cnpj__regex=rf'{cnpj_clean}')
        else:
            parceiros = Parceiro.objects.all()

    return render(request, 'parceiros/consultar_parceiro.html', {
        'form': form,
        'parceiros': parceiros
    })

@login_required
def editar_parceiro(request, cnpj):
    """Edição de parceiros existentes (apenas para colaboradores)"""
    parceiro = get_object_or_404(Parceiro, cnpj=cnpj)
    
    if request.method == 'POST':
        form = ParceiroForm(request.POST, instance=parceiro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parceiro atualizado com sucesso!')
            return redirect('parceiros:consultar_parceiro')
        else:
            messages.error(request, 'Erro ao atualizar parceiro. Verifique os dados informados.')
    else:
        form = ParceiroForm(instance=parceiro)
    
    return render(request, 'parceiros/editar_parceiro.html', {'form': form, 'parceiro': parceiro})

@login_required
def excluir_parceiro(request, cnpj):
    """Exclusão de parceiros (apenas para colaboradores)"""
    parceiro = get_object_or_404(Parceiro, cnpj=cnpj)
    
    if request.method == 'POST':
        if hasattr(parceiro, 'reservas') and parceiro.reservas.exists():
            messages.error(request, 'Não é possível excluir este parceiro pois ele possui reservas associadas.')
            return redirect('parceiros:consultar_parceiro')
        
        try:
            parceiro.delete()
            messages.success(request, 'Parceiro excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir parceiro: {str(e)}')
        
        return redirect('parceiros:consultar_parceiro')
    
    return render(request, 'parceiros/excluir_parceiro.html', {'parceiro': parceiro})
