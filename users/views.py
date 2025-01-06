from django.contrib.auth.views import (
    LoginView as AuthLoginView,
    LogoutView as AuthLogoutView,
)
from django.contrib import messages


class LoginView(AuthLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    next_page = "trips:trip_list"

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(AuthLogoutView):
    next_page = "users:login"
