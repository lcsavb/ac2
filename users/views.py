from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CreateClinic
from django.contrib.auth.decorators import login_required

def sign_up(request):
    '''Afterwards the Clinic and Doctor are created. They are 
    linked to the User with a ManyToMany relationship 
    through the Issuer model. I have decided to use this
    approach to avoid multiple fields for signing up
    and for the sake of simplicity and flexibility.'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Conta criada: {email}!')
            return redirect('users:login')
    else:           
        form = UserRegisterForm()
    return render(request, 'users/sign_up.html', {'form': form})


def login(request):
    return render(request, 'users/login.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def create_clinic(request):
    form = CreateClinic()
    if request.method == 'POST':
        form = CreateClinic(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Clínica cadastrada com sucesso!')
            return redirect('users:profile')
    else:
        form = CreateClinic()

    return render(request, 'users/create_clinic.html', {'form': form})
