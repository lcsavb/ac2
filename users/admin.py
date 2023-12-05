from django.contrib import admin
from .models import CustomUser, Issuer, Doctor, Clinic

# List of models
models = [CustomUser, Issuer, Doctor, Clinic]

# Loop to create an admin class and register each model
for model in models:
    class_name = f"{model.__name__}Admin"
    admin_class = type(class_name, (admin.ModelAdmin,), {})
    admin.site.register(model, admin_class)
