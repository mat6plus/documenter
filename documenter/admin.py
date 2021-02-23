from django.contrib import admin
from .models import Searcher

# Register your models here

@admin.register (Searcher)

class SearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author','created')
    list_filter = ('created', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ('created','updated')

