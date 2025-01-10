from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .models import Trip
from .forms import TripForm


@method_decorator(never_cache, name="dispatch")
class BaseTripView(LoginRequiredMixin):
    pass


class IndexView(BaseTripView, generic.ListView):
    def get_queryset(self):
        trips = Trip.objects.filter(user=self.request.user)
        # TODO: paginate
        return trips.order_by("-id")


class CreateView(BaseTripView, generic.CreateView):
    model = Trip
    form_class = TripForm
    template_name = "trips/new.html"
    success_url = "/trips"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailsView(BaseTripView, generic.DetailView):
    model = Trip

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UpdateView(BaseTripView, generic.UpdateView):
    model = Trip
    form_class = TripForm
    template_name = "trips/edit.html"
    success_url = "/trips"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
