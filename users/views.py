from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
)
from django.contrib import messages
from django.shortcuts import redirect, render

from users.forms import UserRegisterForm


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
