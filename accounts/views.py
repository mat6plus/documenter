from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth.forms import UserCreationForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from accounts.token import account_activation_token

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, FormView
from validate_email import validate_email
from django.urls import reverse

from django.contrib.auth import get_user_model, login
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import SignUpForm, LoginForm, UserEditForm

User = get_user_model()

######################################################################################
class signupView(View):
    def get(self, request):
        return render(request, 'accounts/partials/register.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be atleast 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords dont match')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Please provide a valid email')
            context['has_error'] = True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email already registered by another user')
                context['has_error'] = True

        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'accounts/partials/register.html', context, status=400)

        user = User.objects.create_user(email=email, password = password)
        user.set_password(password)
        user.last_name = last_name
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        subject = 'Active your Account'
        message = render_to_string('accounts/partials/account_activation_email.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   }
                                   )
 
        to_email = request.POST.get('email')  
        email = EmailMessage(  
                subject, message, to=[to_email]  
                )  

        if not context['has_error']:
            email.send()
            messages.add_message(request, messages.SUCCESS,'We sent you an email to verify your account')
            #return render(request, 'accounts/partials/account_activation_sent.html')

        return redirect('accounts:login')


####################################################################################
# class logoutView(View):
#     def post(self, request):
#         logout(request)
#         messages.add_message(request, messages.SUCCESS, 'Successfully logged out')
#         return redirect('accounts:login')

####################################################################################
def logout_request(request):
        logout(request)
        messages.info(request, "You have successfully logged out.") 
        return redirect("accounts:login")

###################################################################################################

#Validation that user exist during login if not it should display associated error of user not existing.

#########################################################################

class loginView(View):
    def get(self, request):
        return render(request, 'accounts/partials//login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == '':
            messages.add_message(request, messages.ERROR,
                                 'Email is required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Password is required')
            context['has_error'] = True
        user = authenticate(request, email=email, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'accounts/partials/login.html', context=context)
        login(request, user)
        #return redirect('documenter:home')
        return render(request, 'documenter/_partials/home.html', context=context)


@login_required
class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/partials/userprofile.html'
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

        messages.success(self.request, ('Profile data has been successfully updated.'))

        return redirect('accounts:change_profile')


def account_activation_sent_view(request):
    return render(request, 'accounts/partials/account_activation_sent.html')

class account_activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
            return redirect('accounts:login')
        return render(request, 'accounts/partials/account_activation_invalid.html', status=401)

