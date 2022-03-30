from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from django_registration.backends.activation.views import RegistrationView

from . import views as account_view

from .forms import QuizRegistrationForm
from .views import QuizRegistrationView

# app_name = "accounts"

urlpatterns = [
    path(
        "register",
        QuizRegistrationView.as_view(),
        name="sign_up",
    ),
    path(
        "password_reset",
        auth_views.PasswordResetView.as_view(
            html_email_template_name="registration/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path("profile/", account_view.profile_redirect_view, name="profile_redirect"),
]
