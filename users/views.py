from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def sign_up(request):
    form = UserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})
