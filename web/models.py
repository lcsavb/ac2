from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from users import models as user_models

JSONField = models.JSONField
BooleanField = models.BooleanField

class Disease(models.Model):
    icd = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=100)
    protocol = models.ForeignKey('Protocol', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.icd} - {self.name}'

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
    social_security_number = models.CharField(max_length=14, unique=True)
    sus_number = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=9)
    telephone = models.CharField(max_length=11)
    telephone_2 = models.CharField(max_length=11)
    user  = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='patients')
    visit = models.ForeignKey('Visit', on_delete=models.PROTECT, null=True)

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
    disease = models.ForeignKey('Disease', on_delete=models.PROTECT)
    posology = JSONField()
    previous_treatment = BooleanField(default=False)
    previous_medications = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now)
    filled_by = models.CharField(max_length=128, choices=(('P', "Patient"), ('C', "Caregiver"), ('M', 'Mother'), ('D', 'Doctor')))
    patient = models.ForeignKey('Patient', on_delete=models.PROTECT)
    issuer = models.ForeignKey(user_models.Issuer, on_delete=models.PROTECT, related_name='prescriptions')
    medication = models.ManyToManyField(Medication, related_name='prescriptions')
    conditional_data = JSONField()
    protocol = models.ForeignKey('Protocol', on_delete=models.PROTECT)
    

    def __str__(self):
        return f'{self.patient} - {self.date} - {self.diagnosis}'

class Protocol(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.CharField(max_length=600)
    medications = models.ManyToManyField('Medication', related_name='protocols')
    conditional_data = JSONField()

    def __str__(self):
        return f'{self.name} - {self.pdf}'

class PatientCareLink(models.Model):
    # Through this model, we will be able to link a patient to a doctor and a clinic
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    issuer = models.OneToOneField(user_models.Issuer, on_delete=models.PROTECT)
    associated_date = models.DateField(default=timezone.now)

class Visit(models.Model):
    date = models.DateField()
    time = models.TimeField()
    link = models.OneToOneField(PatientCareLink, on_delete=models.PROTECT)
    prescription = models.ForeignKey(Prescription, on_delete=models.PROTECT, null=True)
