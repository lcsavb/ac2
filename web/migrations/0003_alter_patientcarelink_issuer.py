# Generated by Django 4.2.7 on 2023-12-16 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_issuer_user_clinic_doctors_customuser_issuer_and_more'),
        ('web', '0002_remove_prescription_visit_patient_visit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientcarelink',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.issuer'),
        ),
    ]