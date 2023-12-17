# Generated by Django 4.2.7 on 2023-12-17 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_issuer_user_clinic_doctors_customuser_issuer_and_more'),
        ('web', '0004_patientcarelink_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='link',
        ),
        migrations.AddField(
            model_name='visit',
            name='issuer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='visits', to='users.issuer'),
        ),
        migrations.DeleteModel(
            name='PatientCareLink',
        ),
    ]
