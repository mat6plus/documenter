import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, login
from django.template.loader import render_to_string
from .forms import SignUpForm

User = get_user_model()


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            login(request, user)
            context = {
                    'email': user.email,
                    'protocol': 'https' if request.is_secure() else "http",
                    'domain': request.get_host(),
                }
            html = render_to_string('accounts/email/welcome.html', context)
            text = render_to_string('accounts/email/welcome.txt', context)
            send_mail(
                    'Welcome to Documenter Appllication!',
                    message=text,
                    html_message=html,
                    recipient_list=[user.email],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    fail_silently=False,
                )
            return redirect('register')
            return redirect('/')
        else:
            return render(request, 'accounts/partials/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'accounts/partials/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return render(request, 'documenter/_partials/home.html')
        if request.method == 'POST':
            email = request.email.POST['email']
            password = request.password.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                return redirect('/')
            else:
                form = AuthenticationForm(request.POST)
                return render (request, 'documenter/_partials/home.html', {'form':form})
