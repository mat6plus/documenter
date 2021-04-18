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
#from validate_email import validate_email
from django.contrib.auth import get_user_model, login
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import SignUpForm, UserEditForm

User = get_user_model()

# def home(request):
#     context=[]
#     return render (request, 'documenter/_partials/home.html')

# def signupView(request):
#     if request.user.is_authenticated:
#         return redirect('documenter:home')
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.profile.first_name = form.cleaned_data.get('first_name')
#             user.profile.last_name = form.cleaned_data.get('last_name')
#             user.profile.email = form.cleaned_data.get('email')
#             user.is_active = False
#             user.save()

#             messages.success(request, "Registration successful. An activation email has been sent" )
#             user.is_active = False
#             current_site = get_current_site(request)

#             subject = 'Activate your Documenter Account'
#             message = render_to_string('accounts/partials/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.send_mail(subject=subject, message=message)
#             messages.SUCCESS(request, f'Registered succesfully and Activation Email Sent')
#             return redirect('accounts/partials/account_activation_sent.html')
            
#             # context = {
#             #         'email': user.email,
#             #         'protocol': 'https' if request.is_secure() else "http",
#             #         'domain': request.get_host(),
#             #     }
#             # html = render_to_string('accounts/email/welcome.html', context)
#             # text = render_to_string('accounts/email/welcome.txt', context)
#             # send_mail(
#             #         'Welcome to Documenter Appllication!',
#             #         message=text,
#             #         html_message=html,
#             #         recipient_list=[user.email],
#             #         from_email=settings.DEFAULT_FROM_EMAIL,
#             #         fail_silently=False,
#             #     )
#             # # return HttpResponse('User Succesfully Registered')
#             # return redirect('accounts:login')
#         # else:
#         #     return render(request, 'accounts/partials/register.html', {'form': form})
#     else:
#         # messages.ERROR(request, 'Registration Failed, kindly check your Informations')
#         form = SignUpForm()
#     return render(request, 'accounts/partials/register.html', {'form': form})
#####################################################################################################

def signupView(request):  
    if request.method == 'GET':  
        return render(request, 'accounts/partials/register.html')  
    if request.method == 'POST':  
        form = SignUpForm(request.POST)   
        if form.is_valid():  
            user = form.save(commit=True)  
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Activate your account.'  
            message = render_to_string('accounts/partials/account_activation_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),  
                'token': account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
        else:  
            form = SignUpForm()  
        return render(request, 'accounts/partials/register.html', {'form': form})  

######################################################################################



####################################################################################
        

def loginView(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


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


# def account_activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('documenter:landing.html')
#     else:
#         return render(request, 'accounts/account_activation_invalid.html')

def account_activate(request, uidb64, token):  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')

