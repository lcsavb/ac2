from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ac2.decorators import clinic_required
from .forms import UserRegisterForm, CreateClinic, CreateDoctor

def sign_up(request):
    '''Afterwards the Doctor is created. They are 
    linked to the User with a ManyToMany relationship 
    through the Issuer model. I have decided to use this
    approach to avoid multiple fields for signing up
    and for the sake of simplicity and flexibility.'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
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

def create_profile(request, form_class, template_name, success_message, success_url):
    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, success_message)
        return redirect(success_url)

    return render(request, template_name, {'form': form})

@login_required
def create_clinic(request):
    return create_profile(
        request,
        CreateClinic,
        'users/create_clinic.html',
        'Clínica cadastrada com sucesso!',
        'users:create_doctor'
    )

@login_required
@clinic_required
def create_doctor(request):
    return create_profile(
        request,
        CreateDoctor,
        'users/create_doctor.html',
        'Médico cadastrado com sucesso!',
        'users:profile'
    )