from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from documenter.models import Searcher
from accounts.models import Profile, User

User = get_user_model()

class SearchForm(ModelForm):
    query = forms.CharField()

class DocumentForm(ModelForm):
    class Meta:
        model = Searcher
        field = '__all__'
        exclude = ['slug']
       # field_classes = {'slug': slug,}





# SearchForm, DocumentationForm | Title, Tag, Description, Images#