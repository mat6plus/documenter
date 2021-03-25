import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from django.forms import ValidationError
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.shortcuts import render,redirect, get_object_or_404
from accounts.token import account_activation_token
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib import messages
from validate_email import validate_email

from django.conf import settings
from django.views.generic import View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, login
from django.template.loader import render_to_string
from .forms import SignUpForm, UserEditForm

User = get_user_model()


def signupView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password')

            if password != password2:
                messages.add_message(request, messages.ERROR, 'Password do not match')
            
            if not validate_email(email):
                messages.add_message(request, messages.ERROR, 'Please Enter a Valid Email')
            
            if User.objects.filter(email).exist():
                messages.add_message(request, messages.ERROR, 'Email Already Exist, Choose Another')

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

def loginView(request):
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
                return render (request, 'documenter/partials/home.html', {'form':form})

class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/partials/profile.html'
    form_class = UserEditForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect('accounts:change_profile')

def account_activation_sent_view(request):
    return render(request, 'accounts/partials/account_activation_sent.html')


def account_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('documenter:landing.html')
    else:
        return render(request, 'accounts/account_activation_invalid.html')