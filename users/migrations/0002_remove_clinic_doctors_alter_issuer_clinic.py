# Generated by Django 4.2.7 on 2023-12-15 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinic',
            name='doctors',
        ),
        migrations.AlterField(
            model_name='issuer',
            name='clinic',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='users.clinic'),
        ),
    ]