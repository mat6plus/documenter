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
                messages.add_message(request, messages.ERROR, 'Password Mismatch')
            
            if not validate_email(email):
                messages.add_message(request, messages.ERROR, 'Please Enter a Valid Email')
            
            if User.objects.filter(email).exist():
                messages.add_message(request, messages.ERROR, 'Email Already Exist, Choose Another')

            user = User.objects.create_user(email=email, password=password)
 #           login(request, user)
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