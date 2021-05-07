from django.urls import path
from . import views
from accounts.views import *
#from accounts.views import signupView, loginView, logoutUser, ChangeProfileView, account_activation_sent_view
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
# from django.contrib.auth.views import LoginView, LogoutView, 
#     PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
#     PasswordResetDoneView

app_name = 'accounts'


urlpatterns = [

    path('', loginView.as_view(), name='login'),
    # path('', views.loginView, name='login'),

    path('activate/<uidb64>/<token>',
         views.account_activate.as_view(), name='activate'),

    path('register/', signupView.as_view(), name='register'),

    path('logout/', logoutView.as_view(), name='logout'),
   # path("logout/", views.logoutUser, name="logout"),

    path('password_reset/', PasswordResetView.as_view(
        template_name='accounts/partials/password_reset.html',
        email_template_name='accounts/email/password_reset.txt',
        html_email_template_name='accounts/email/password_reset_email.html',
        subject_template_name='accounts/email/password_reset_subject.txt'
    ), name='password_reset'),

    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='accounts/partials/password_reset_done.html',
        ),
        name='password_reset_done'),

    path(
        'password_reset/<str:uidb64>/<str:token>/',
        PasswordResetConfirmView.as_view(
            template_name='accounts/partials/password_reset_confirm.html',
        ),
        name='password_reset_confirm'),

    path(
        'password_reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='accounts/partials/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
]
