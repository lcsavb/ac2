from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# There is a need to add a new row: which user created the entry.

class Issuer(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT, null=True)
    clinic = models.ForeignKey('Clinic', on_delete=models.PROTECT, null=True)
    
class Clinic(models.Model):
    name = models.CharField(max_length=100)
    #API (DataSUS) ---> https://apidadosabertos.saude.gov.br/v1/#/CNES/get_cnes_estabelecimentos. 
    sus_number = models.CharField(max_length=7, primary_key=True)
    address = models.CharField(max_length=100)
    address_number = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=9)
    phone = models.CharField(max_length=100)
    doctors = models.ManyToManyField('Doctor', through='Issuer', related_name='clinics')

    def __str__(self):
        return f"{self.name} - {self.sus_number}"

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    council_number = models.CharField(max_length=100)
    sus_number = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    
    def __str__(self):
        return self.council_number


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    clinic = models.ManyToManyField('Clinic', related_name='users', blank=True)
    issuer = models.ManyToManyField('Issuer', related_name='users', blank=True)  

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_user_permissions",
        related_query_name="customuser",
    )

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('custom user')
        verbose_name_plural = _('custom users')