from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
)
from django.shortcuts import redirect, render
from django.db import transaction

from users.forms import UserRegisterForm, UserUpdateForm, UserSettingsForm
from users.models import UserSetting


class LoginView(AuthLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    next_page = "trips:trip_list"

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(AuthLogoutView):
    next_page = "users:login"


def signup(request):
    if request.method == "GET":
        form = UserRegisterForm()
        return render(request, "signup.html", {"form": form})

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            messages.success(
                request, "Congratulations! You have signed up successfully."
            )

            login(request, user)

            return redirect("trips:trip_list")
        else:
            return render(request, "signup.html", {"form": form})


@login_required
def profile(request):
    user_settings, _ = UserSetting.objects.get_or_create(user=request.user)

    if request.method == "GET":
        user_form = UserUpdateForm(instance=request.user)
        user_settings_form = UserSettingsForm(instance=user_settings)
        return render(
            request,
            "profile.html",
            {"user_form": user_form, "user_settings_form": user_settings_form},
        )

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        user_settings_form = UserSettingsForm(request.POST, instance=user_settings)

        if user_form.is_valid() and user_settings_form.is_valid():
            # attempt to update both models in a transaction
            with transaction.atomic():
                user_form.save()
                user_settings_form.save()

            messages.success(request, "Your profile has been updated successfully.")
            return redirect("users:profile")
        else:
            return render(
                request,
                "profile.html",
                {"user_form": user_form, "user_settings_form": user_settings_form},
            )
