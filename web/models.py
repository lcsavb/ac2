from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    # The base user is always the clinic, however I am using a one to one relationship due to django's authentication system.
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    clinic = models.OneToOneField(Clinic, on_delete=models.CASCADE, related_name='user')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    council_number = models.CharField(max_length=100)
    sus_number = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    clinics = models.ManyToManyField(Clinic, through='Issuer', related_name='doctors')
    patients = models.ManyToManyField(Patient, through='PatientCareLink', related_name='doctors')

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
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='patients')

    def __str__(self):
        return self.social_security_number

class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    formulation = models.CharField(max_length=100, blank=True)

    # Here I think I should add  the FIHR id of the medication.

    def __str__(self):
        return f'{self.name} - {self.dosage} - {self.formulation}'

class Prescription(models.Model):
    anamnesis = models.TextField(max_length=1000)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medication, related_name='prescriptions')
    prescription = JSONField()
    previous_treatment = BooleanField(default=False)
    previous_medications = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now)
    filled_by = models.CharField(choices=(('P', "Patient"), ('C', "Caregiver"),('M', 'Mother'), ('D', 'Doctor'), max_length=128)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    medication = models.ManyToManyField(Medication, related_name='prescriptions')
    conditional_data = JSONField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='prescriptions')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='prescriptions')

    def __str__(self):
        return f'{self.patient} - {self.date} - {self.diagnosis}'

class Protocol(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.CharField(max_length=600)
    medications = models.ManyToManyField(Medication, related_name='protocols')
    conditional_data = JSONField()
    prescription = models.ManyToManyField(Prescription, related_name='protocols')

    def __str__(self):
        return f'{self.name} - {self.pdf}'

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    # SUS means Unified Health System and the "SUS number" (Cartão Nacional de Saúde) is a unique number for each entity or person registered in the system. There is an API to retrieve the data and check it (DataSUS).
    sus_number = models.CharField(max_length=7)
    address = models.CharField(max_length=100)
    address_number = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=9)
    phone = models.CharField(max_length=100)
    # I forgot what related_name does. I think it is used to access the clinics from the doctor model.
    doctors = models.ManyToManyField(Doctor, through='Issuer', related_name='clinics')
    patients = models.ManyToManyField(Patient)

class PatientCareLink(models.Model):
    # Through this model, we will be able to link a patient to a doctor and a clinic
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT)
    associated_date = models.DateField(default=timezone.now)

class Issuer(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT)
    patient = models.ManyToManyField(Patient, through='Prescription', through_fields=('issuer', 'patient'), related_name='issuer')

class Visit(models.Model):
    date = models.DateField()
    time = models.TimeField()
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    link = models.ManytoOneField(PatientCareLink, on_delete=models.CASCADE)

