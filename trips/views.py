from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .models import Trip
from .forms import TripForm
from users.models import User


@method_decorator(never_cache, name="dispatch")
class BaseTripView(LoginRequiredMixin):
    pass


class IndexView(BaseTripView, generic.ListView):
    def get_queryset(self):
        # TODO: filter by user once logging in is implemented
        return Trip.objects.order_by("-id")[:5]


class CreateView(BaseTripView, generic.CreateView):
    model = Trip
    form_class = TripForm
    template_name = "trips/new.html"
    success_url = "/trips"

    def form_valid(self, form):
        # TODO: change this to request.user once logging in is implemented
        form.instance.user = User.objects.first()
        return super().form_valid(form)


class DetailsView(BaseTripView, generic.DetailView):
    # TODO: 403 if user is not the owner of the trip
    model = Trip


class UpdateView(BaseTripView, generic.UpdateView):
    model = Trip
    form_class = TripForm
    template_name = "trips/edit.html"
    success_url = "/trips"
