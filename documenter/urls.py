from django.urls import path

from .views import searchview 


urlpatterns = [
    path('', searchview, name='home'),
]