from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

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
            return redirect('web-home')
    else:           
        form = UserRegisterForm()
    return render(request, 'users/sign_up.html', {'form': form})
