# Generated by Django 4.2.7 on 2024-01-06 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_patient_issuer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='posology',
            field=models.JSONField(null=True),
        ),
    ]
