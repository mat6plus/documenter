from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.

class Searcher (models.Model):
    title = models.CharField(max_length=250, default=None)
    slug = models.SlugField(max_length=250, unique_for_date='created', default=None)
    description = models.TextField(default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='document_posts', default=None)
    solution_image = models.ImageField()

    tags = TaggableManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
            return reverse('title:description', args=[self.created.year, self.created.month, self.created.day, self.slug])

