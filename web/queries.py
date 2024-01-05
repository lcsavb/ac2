from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Patient 

@login_required
def get_patients(request):
    logged_user = request.user
    issuers = logged_user.issuer.all()
    patients = Patient.objects.filter(issuer__in=issuers, user=logged_user)
    return JsonResponse({'patients': list(patients.values())})


