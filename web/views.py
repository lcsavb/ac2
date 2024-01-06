from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreatePatient, CreatePrescription

def home(request):
    return render (request, 'web/home.html')

@login_required
def create_patient(request):
    form = CreatePatient(request.POST or None, user = request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Paciente criado com sucesso')
        return redirect('new-prescription') 

    return render(request, 'web/create_patient.html', {'form': form})

@login_required
def new_prescription(request):
    form = CreatePrescription(request.POST or None, user = request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Prescrição criada com sucesso')
        return redirect('home')
    return render (request, 'web/new_prescription.html', {'form': form})

