from django.shortcuts import redirect
from django.contrib import messages


def clinic_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.clinic.count() == 0:
            messages.warning(request, f'Você precisa cadastrar uma clínica antes de cadastrar um médico.')
            return redirect('users:create_clinic')
        return view_func(request, *args, **kwargs)
    return _wrapped_view