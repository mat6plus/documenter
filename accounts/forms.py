from django import forms
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from accounts.models import *
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


# class AuthForm(AuthenticationForm):
#     username = forms.EmailField(max_length=254, required=True, help_text='Required. Input a valid email address.')
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Fisrt Name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last Name.')
   # username = forms.EmailField(max_length=254, required=True, help_text='Required. Input a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2',]

    
        def clean_email(self):
            """Ensure email uniqueness."""
            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("Email Already Exist")
            return email

        def clean_password2(self):
                cd = super().clean()
                password1 = cd.get("password1")
                password2 = cd.get("password2")

                if password1 is not None and password1 != password2:
                    raise forms.ValidationError('Passwords don\'t match.')
                return cd
    
    class UserAdminCreationForm(forms.ModelForm):
        first_name = forms.CharField(max_length=30, required=True, help_text='Fisrt Name.')
        last_name = forms.CharField(max_length=30, required=True, help_text='Last Name.')
     # username = forms.EmailField(max_length=254, required=True, help_text='Required. Input a valid email address.')
        password1 = forms.CharField(widget=forms.PasswordInput)
        password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

        class Meta:
            model = CustomUser
            fields = ['email']
        
        def clean_password2(self):
            cd = super().clean()
            password1 = cd.get("password1")
            password2 = cd.get("password2")

            if password1 is not None and password1 != password2:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cd["password1"])

            if commit:
                user.save()
            return user
    
    class UnserAdminChangeForm(forms.ModelForm):
        password = ReadOnlyPasswordHashField()

        class Meta:
            model = CustomUser
            fields = ['email', 'password', 'is_active', 'admin']

            def clean_password(self):
                return self.initial["password"]
            
          

    
    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=True)
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.email = self.cleaned_data['email']
        
    #     if commit:
    #         user.save()
    #     return user
""" 
class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email' ) """
    

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)


# class PwdResetForm(PasswordResetForm):
    
#     email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         u = User.objects.filter(email=email)
#         if not u:
#             raise forms.ValidationError(
#                 'Unfortunatley we can not find that email address')
#         return email

# class UserEditForm(forms.ModelForm):
    
#     email = forms.EmailField(
#         label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
#             attrs={'placeholder': 'email', 'readonly': 'readonly'}))

#     first_name = forms.CharField(
#         label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
#             attrs={'placeholder': 'Username','readonly': 'readonly'}))

#     last_name = forms.CharField(
#         label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
#             attrs={'placeholder': 'Firstname'}))

#     class Meta:
#         model = Profile
#         fields = ('email', 'first_name', 'last_name',)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.fields['email'].required = True

