def signupView(request):
    
    if request.user.is_authenticated:
        return redirect('documenter:home')

    if request.method == 'POST':
        registerForm = SignUpForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
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