from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreatePatient

def home(request):
    return render (request, 'web/home.html')

def create_patient(request):
    form = CreatePatient(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Paciente criado com sucesso')
        return redirect('new-prescription') 

    return render(request, 'web/create_patient.html', {'form': form})

def new_prescription(request):
    return render (request, 'web/new_prescription.html')

