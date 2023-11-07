from .views import (
    EmailValidationView,
    LoginView,
    LogoutView,
    RegistrationView,
    UsernameValidationView,
    VerificationView,
)
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("inscription", RegistrationView.as_view(), name="inscription"),
    path("connexion", LoginView.as_view(), name="connexion"),
    path("logout", LogoutView.as_view(), name="logout"),
    path(
        "validation-utilisateur",
        csrf_exempt(UsernameValidationView.as_view()),
        name="validation-utilisateur",
    ),
    path(
        "validation-email",
        csrf_exempt(EmailValidationView.as_view()),
        name="validation-email",
    ),
    path(
        "activercompte/<uidb64>/<token>",
        VerificationView.as_view(),
        name="activercompte",
    ),
]
