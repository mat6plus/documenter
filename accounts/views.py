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
from django.contrib.auth import get_user_model, login
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import SignUpForm, UserEditForm



def home(request):
    context=[]
    return render (request, 'documenter/_partials/home.html')

def signupView(request):
    if request.user.is_authenticated:
        return redirect('documenter:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()

            messages.success(request, "Registration successful. An activation email has been sent" )
            user.is_active = False
            current_site = get_current_site(request)

            subject = 'Activate your Documenter Account'
            message = render_to_string('accounts/partials/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.send_mail(subject=subject, message=message)
            messages.SUCCESS(request, f'Registered succesfully and Activation Email Sent')
            return redirect('accounts/partials/account_activation_sent.html')
            
            # context = {
            #         'email': user.email,
            #         'protocol': 'https' if request.is_secure() else "http",
            #         'domain': request.get_host(),
            #     }
            # html = render_to_string('accounts/email/welcome.html', context)
            # text = render_to_string('accounts/email/welcome.txt', context)
            # send_mail(
            #         'Welcome to Documenter Appllication!',
            #         message=text,
            #         html_message=html,
            #         recipient_list=[user.email],
            #         from_email=settings.DEFAULT_FROM_EMAIL,
            #         fail_silently=False,
            #     )
            # # return HttpResponse('User Succesfully Registered')
            # return redirect('accounts:login')
        # else:
        #     return render(request, 'accounts/partials/register.html', {'form': form})
    else:
        # messages.ERROR(request, 'Registration Failed, kindly check your Informations')
        form = UserCreationForm()
    return render(request, 'accounts/partials/register.html', {'form': form})


# def signupView(request):
# 	if request.method == "POST":
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			login(request, user)
# 			messages.success(request, "Registration successful." )
# 			return redirect("accounts:login")
# 		messages.error(request, "Unsuccessful registration. Invalid information.")
# 	form = SignUpForm
# 	return render (request=request, template_name="accounts/partials/register.html", context={"register_form":form})
        

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

# @login_required(login_url='login')
# def home(request):
# 	orders = Order.objects.all()
# 	customers = Customer.objects.all()

# 	total_customers = customers.count()

# 	total_orders = orders.count()
# 	delivered = orders.filter(status='Delivered').count()
# 	pending = orders.filter(status='Pending').count()

# 	context = {'orders':orders, 'customers':customers,
# 	'total_orders':total_orders,'delivered':delivered,
# 	'pending':pending }

# 	return render(request, 'accounts/dashboard.html', context)

# @login_required(login_url='login')
# def products(request):
# 	products = Product.objects.all()

# 	return render(request, 'accounts/products.html', {'products':products})

# @login_required(login_url='login')
# def customer(request, pk_test):
# 	customer = Customer.objects.get(id=pk_test)

# 	orders = customer.order_set.all()
# 	order_count = orders.count()

# 	myFilter = OrderFilter(request.GET, queryset=orders)
# 	orders = myFilter.qs 

# 	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
# 	'myFilter':myFilter}
# 	return render(request, 'accounts/customer.html',context)

# @login_required(login_url='login')
# def createOrder(request, pk):
# 	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
# 	customer = Customer.objects.get(id=pk)
# 	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
# 	#form = OrderForm(initial={'customer':customer})
# 	if request.method == 'POST':
# 		#print('Printing POST:', request.POST)
# 		form = OrderForm(request.POST)
# 		formset = OrderFormSet(request.POST, instance=customer)
# 		if formset.is_valid():
# 			formset.save()
# 			return redirect('/')

# 	context = {'form':formset}
# 	return render(request, 'accounts/order_form.html', context)

# @login_required(login_url='login')
# def updateOrder(request, pk):

# 	order = Order.objects.get(id=pk)
# 	form = OrderForm(instance=order)

# 	if request.method == 'POST':
# 		form = OrderForm(request.POST, instance=order)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')

# 	context = {'form':form}
# 	return render(request, 'accounts/order_form.html', context)

# @login_required(login_url='login')
# def deleteOrder(request, pk):
# 	order = Order.objects.get(id=pk)
# 	if request.method == "POST":
# 		order.delete()
# 		return redirect('/')

# 	context = {'item':order}
# 	return render(request, 'accounts/delete.html', context)