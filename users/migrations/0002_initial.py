# Generated by Django 4.2.7 on 2023-11-22 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('web', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuer',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.clinic'),
        ),
        migrations.AddField(
            model_name='issuer',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.doctor'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_groups', related_query_name='customuser', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='issuer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.issuer'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_user_permissions', related_query_name='customuser', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
