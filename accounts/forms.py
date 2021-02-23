from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')
    
        def clean_email(self):
            """Ensure email uniqueness."""
            email = self.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("The email address provided is currently by another account.")
            return email

        def clean_password2(self):
                cd = self.cleaned_data
                if cd['password'] != cd['password2']:
                 raise forms.ValidationError('Passwords don\'t match.')
                return cd['password2']
""" 
class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email' ) """
    

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)


class PwdResetForm(PasswordResetForm):
    
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

class UserEditForm(forms.ModelForm):
    
    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'placeholder': 'email', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'placeholder': 'Username','readonly': 'readonly'}))

    last_name = forms.CharField(
        label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'placeholder': 'Firstname'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True