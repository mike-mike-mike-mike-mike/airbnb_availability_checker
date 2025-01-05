from django.views import generic
from django.contrib.auth.models import User

from .models import Trip
from .forms import TripForm


class IndexView(generic.ListView):
    def get_queryset(self):
        # TODO: filter by user once logging in is implemented
        return Trip.objects.order_by("-id")[:5]


class CreateView(generic.CreateView):
    model = Trip
    form_class = TripForm
    template_name = "trips/new.html"
    success_url = "/trips"

    def form_valid(self, form):
        # TODO: change this to request.user once logging in is implemented
        form.instance.user = User.objects.first()
        return super().form_valid(form)


class DetailsView(generic.DetailView):
    # TODO: 403 if user is not the owner of the trip
    model = Trip


class UpdateView(generic.UpdateView):
    model = Trip
    form_class = TripForm
    template_name = "trips/edit.html"
    success_url = "/trips"
