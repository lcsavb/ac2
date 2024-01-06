from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Patient 

@login_required
def get_patients(request, issuer_id):
    logged_user = request.user
    patients = Patient.objects.filter(issuer__id=issuer_id, user=logged_user)
    patients_list = [{'id': patient.id, 'name': str(patient)} for patient in patients]
    return JsonResponse({'patients': patients_list})

@login_required
def get_issuers(request):
    logged_user = request.user
    issuers = logged_user.issuer.all()
    issuers_list = [{'id': issuer.id, 'name': str(issuer)} for issuer in issuers]
    return JsonResponse({'issuers': issuers_list})


