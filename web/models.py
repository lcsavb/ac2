from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from users.models import Issuer

JSONField = models.JSONField
BooleanField = models.BooleanField

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    #API (DataSUS) ---> https://apidadosabertos.saude.gov.br/v1/#/CNES/get_cnes_estabelecimentos. 
    sus_number = models.CharField(max_length=7)
    address = models.CharField(max_length=100)
    address_number = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=9)
    phone = models.CharField(max_length=100)
    doctors = models.ManyToManyField('Doctor', through=Issuer)
    patients = models.ManyToManyField('Patient')

class Disease(models.Model):
    icd = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=100)
    protocol = models.ForeignKey('Protocol', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.icd} - {self.name}'


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    council_number = models.CharField(max_length=100)
    sus_number = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    clinics = models.ManyToManyField(Clinic, through=Issuer)
    patients = models.ManyToManyField('Patient', through='PatientCareLink')

    def __str__(self):
        return self.council_number

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    disabled = models.BooleanField()
    responsible = models.CharField(max_length=100)
    identity = models.CharField(max_length=100)
    weight = models.FloatField()
    height = models.FloatField()
    ethnicity = models.CharField(max_length=100)
    social_security_number = models.CharField(max_length=14)
    sus_number = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=9)
    telephone = models.CharField(max_length=11)
    telephone_2 = models.CharField(max_length=11)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.social_security_number

class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    formulation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name} - {self.dosage} - {self.formulation}'

class Prescription(models.Model):
    anamnesis = models.TextField(max_length=1000)
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE)
    posology = JSONField()
    previous_treatment = BooleanField(default=False)
    previous_medications = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now)
    filled_by = models.CharField(max_length=128, choices=(('P', "Patient"), ('C', "Caregiver"), ('M', 'Mother'), ('D', 'Doctor')))
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    medication = models.ManyToManyField(Medication)
    conditional_data = JSONField()
    doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT)
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient} - {self.date} - {self.diagnosis}'

class Protocol(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.CharField(max_length=600)
    medications = models.ManyToManyField('Medication')
    conditional_data = JSONField()
    prescription = models.ManyToManyField(Prescription)

    def __str__(self):
        return f'{self.name} - {self.pdf}'

class PatientCareLink(models.Model):
    # Through this model, we will be able to link a patient to a doctor and a clinic
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT)
    associated_date = models.DateField(default=timezone.now)

class Visit(models.Model):
    date = models.DateField()
    time = models.TimeField()
    link = models.ForeignKey(PatientCareLink, on_delete=models.PROTECT)
