from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from accounts.managers import CustomUserManager
from django_countries.fields import CountryField


# Create your models here.

# class CustomUser(AbstractUser):

#     email = models.EmailField(_('email address'), unique=True)
#     first_name = models.CharField(max_length=150, unique=True)
#     last_name = models.CharField(max_length=150, blank=True)
#     about = models.TextField(_('about'), max_length=500, blank=True)
#     country = CountryField()

#     # User Status
#     is_active = models.BooleanField(default=False)
#     signup_confirmation = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     class Meta:
#         verbose_name = _("user")
#         verbose_name_plural = _("users")

#     username = None
#     email = models.EmailField(_("email address"), unique=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)
    country = CountryField()

    # User Status
    is_active = models.BooleanField(default=False)
    signup_confirmation = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "accounts"
        verbose_name_plural = "accounts"

    # def __str__(self):
    #     return self.first_name
