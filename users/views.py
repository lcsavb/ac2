from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserRegisterForm

def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f'Conta criada: {username}!')
            return redirect('web-home')
    else:           
        form = UserRegisterForm()
    return render(request, 'users/sign_up.html', {'form': form})
