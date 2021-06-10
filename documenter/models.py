from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from accounts.managers import CustomUserManager
from accounts.models import CustomUser
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.
class Searcher (models.Model):
    title = models.CharField(max_length=250, default=None)
    slug = models.SlugField(max_length=250, unique_for_date='created', default=None)
    description = models.TextField(default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    solution_image = models.ImageField(default=None)
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    tags = TaggableManager()
    

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
    
    def get_full_name(self):
        return f'{self.first_name}+{self.last_name}'
    
    def get_absolute_url(self):
            return reverse('title:description', args=[self.created.year, self.created.month, self.created.day, self.slug])