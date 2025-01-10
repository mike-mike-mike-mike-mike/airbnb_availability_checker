from django.urls import path

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
]
