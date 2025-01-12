from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import LoginView, LogoutView, signup

app_name = "users"
urlpatterns = [
    path(
        "auth/login/",
        LoginView.as_view(),
        name="login",
    ),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path(
        "auth/reset_password/",
        PasswordResetView.as_view(
            template_name="auth/password_reset.html",
            email_template_name="auth/password_reset/email.html",
            success_url="/auth/reset_password/sent/",
        ),
        name="reset_password",
    ),
    path(
        "auth/reset_password/sent/",
        PasswordResetDoneView.as_view(template_name="auth/password_reset/sent.html"),
        name="reset_password_sent",
    ),
    path(
        "auth/reset_password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="auth/password_reset/confirm.html",
            success_url="/auth/reset_password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "auth/reset_password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="auth/password_reset/complete.html"
        ),
        name="password_reset_complete",
    ),
]
