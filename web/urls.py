from django.urls import path
from . import views
from .queries import get_patients, get_issuers

urlpatterns = [
        path('', views.home, name='web-home'),
        path('new-prescription/', views.new_prescription, name='new-prescription'),
        path('create-patient/', views.create_patient, name='create-patient'),
        path('queries/get-patients/<int:issuer_id>/', get_patients, name='get-patients'),
        path('queries/get-issuers/', get_issuers, name='get-issuers'),
        ] 
