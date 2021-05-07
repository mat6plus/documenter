from django.urls import path
from . import views
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from documenter.views import *


urlpatterns = [
    path('home/', searchView, name='home'),
    #path('home/', homeView.as_view(), name='home'),
    path('result/', SearchResultView, name='result'),
    path('details/', SearchDetails, name='details'),
]

app_name = 'documenter'