from django.urls import path

from documenter.views import searchView, SearchResultView, SearchDetails


urlpatterns = [
    path('', searchView, name='home'),
    path('result/', SearchResultView, name='result'),
    path('details/', SearchDetails, name='details'),
]