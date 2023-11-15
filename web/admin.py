from django.contrib import admin
from .models import Clinic, Disease, Doctor, Patient, Medication, Prescription, Protocol, PatientCareLink, Issuer, Visit


# Register your models here.

class ClinicAdmin(admin.ModelAdmin):
    pass

class DiseaseAdmin(admin.ModelAdmin):
    pass

class DoctorAdmin(admin.ModelAdmin):
    pass

class PatientAdmin(admin.ModelAdmin):
    pass

class MedicationAdmin(admin.ModelAdmin):
    pass

class PrescriptionAdmin(admin.ModelAdmin):  
    pass

class ProtocolAdmin(admin.ModelAdmin):  
    pass

class PatientCareLinkAdmin(admin.ModelAdmin):   
    pass

class IssuerAdmin(admin.ModelAdmin):   
    pass

class VisitAdmin(admin.ModelAdmin):   
    pass


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(PatientCareLink, PatientCareLinkAdmin)
admin.site.register(Issuer, IssuerAdmin)
admin.site.register(Visit, VisitAdmin)

