from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Issuer(models.Model):
    doctor = models.ForeignKey('web.Doctor', on_delete=models.PROTECT)
    clinic = models.ForeignKey('web.Clinic', on_delete=models.PROTECT)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
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