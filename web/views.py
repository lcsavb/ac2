from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render (request, 'web/home.html')

def new_prescription(request):
    return render (request, 'web/new_prescription.html')

