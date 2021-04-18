from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
#from django_countries.fields import CountryField
#from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin



class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must provide a Valid Email Address')
        
        user = self.model(email=self.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password,)
        user.staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password,)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    objects = UserManager()





# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField('email address', unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=True)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=150, default=False)
#     signup_confirmation = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.user.first_name} Profile'
    
#     @receiver(post_save, sender=User)
#     def update_profile_signal(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)
#         instance.profile.save()

#     def save(self):
#         super().save()