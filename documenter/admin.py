from django.contrib import admin
from documenter.models import Searcher
from accounts.models import CustomUser

# Register your models here

@admin.register (Searcher )

class SearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','created','author','tags')
    list_filter = ('created','title')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ('created','updated')

