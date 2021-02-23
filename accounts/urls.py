from django.urls import path
from .views import signup
from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetDoneView

app_name = 'accounts'


urlpatterns = [

    path('', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='accounts/partials/login.html',
    ), name='login'),

    path('signup/', signup, name='signup'),

    path('logout/', LogoutView.as_view(), name='logout'),

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
]
