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
from django.contrib.sites.shortcuts import get_current_site
from accounts.token import account_activation_token
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib import messages
from validate_email import validate_email
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text

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

''' def homePage(request):
    context=[]
    return render (request, 'documenter/_partials/home.html')
 '''

def signupView(request):
    
    if request.user.is_authenticated:
        return redirect('documenter:home')

    if request.method == 'POST':
        registerForm = SignUpForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.first_name = registerForm.cleaned_data['first_name']
            user.last_name = registerForm.cleaned_data['last_name']
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('accounts/partials/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('Registered succesfully and Activation sent')
    else:
        registerForm = SignUpForm()
    return render(request, 'accounts/partials/register.html', {'form': registerForm})

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