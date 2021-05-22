from django.urls import path
from . import views
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from documenter.views import *


urlpatterns = [
    path('home/', views.homeView, name='home'),
    path('search/', views.searchView, name='search'),
    path('result/', views.SearchResultView, name='result'),
    path('details/', views.SearchDetails, name='details'),
]

app_name = 'documenter'