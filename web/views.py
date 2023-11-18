from django.shortcuts import render
from forms import CustomUserCreationForm
from models import CustomUser

class SignUp(CustomUserCreationForm):
    clinic_sus_number = forms.CharField(max_length=100)
    clinic_name = forms.CharField(max_length=100)
    clinic_address = forms.CharField(max_length=100)
    clinic_address_number = forms.CharField(max_length=100)
    clinic_phone = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta(CustomUserCreationForm.Meta):
        model = CustomUser 
        fields = ['clinic_sus_number', 'clinic_name', 'clinic_address', 'clinic_address_number', 'clinic_phone', 'email', 'password1', 'password2']
    
