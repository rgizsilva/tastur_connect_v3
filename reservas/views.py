from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from clientes.models import Cliente
from parceiros.models import Parceiro
from .forms import ReservaForm, ConsultaReservaForm
from django.db.models import Q

@login_required
def cadastrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cpf_cliente = form.cleaned_data['cpf_cliente']  
            reserva.save()
            return redirect('reservas:consultar_reserva')  
    else:
        form = ReservaForm()

    return render(request, 'reservas/cadastrar_reserva.html', {'form': form})

def consultar_reserva(request):
    form = ConsultaReservaForm(request.GET or None)
    reservas = Reserva.objects.none()

    if form.is_valid():
        numero_reserva = form.cleaned_data.get('numero_reserva')
        cpf_cliente = form.cleaned_data.get('cpf_cliente')  

        if numero_reserva:
            reservas = Reserva.objects.filter(numero_reserva=numero_reserva)
        elif cpf_cliente:
            reservas = Reserva.objects.filter(
                Q(cpf_cliente__cpf_cliente__icontains=cpf_cliente)
            )

    return render(request, 'reservas/consultar_reserva.html', {'form': form, 'reservas': reservas})

@login_required
def editar_reserva(request, numero_reserva):
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva editada com sucesso!")
            return redirect('reservas:consultar_reserva')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'reservas/cadastrar_reserva.html', {'form': form, 'reserva': reserva})

@login_required
def excluir_reserva(request, numero_reserva):
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva excluída com sucesso!")
        return redirect('reservas:consultar_reserva')
    
    return render(request, 'reservas/excluir_reserva.html', {'reserva': reserva})
