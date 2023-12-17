from django.contrib import admin
from .models import Disease, Patient, Medication, Prescription, Protocol, Visit

# List of models
models = [Disease, Patient, Medication, Prescription, Protocol, Visit]

# Loop to create an admin class and register each model
for model in models:
    class_name = f"{model.__name__}Admin"
    admin_class = type(class_name, (admin.ModelAdmin,), {})
    admin.site.register(model, admin_class)
