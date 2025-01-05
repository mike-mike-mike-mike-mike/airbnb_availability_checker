from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from .models import Trip


class IndexView(generic.ListView):
    def get_queryset(self):
        return Trip.objects.order_by("-id")[:5]


def new(request, error_message=None):
    return render(request, "trips/new.html", {"error_message": error_message})


def create(request):
    try:
        room_id = request.POST["room_id"]
        check_in = request.POST["check_in"]
        check_out = request.POST["check_out"]

        trip = Trip(room_id=room_id, check_in=check_in, check_out=check_out)
        trip.save()

        return HttpResponseRedirect(reverse("trips:show", args=(trip.id)))
    except Exception as e:
        # re-render the new form with the error message
        return new(request, error_message=str(e))


class DetailsView(generic.DetailView):
    model = Trip


def edit(request, trip_id):
    return HttpResponse(f"You're editing trip {trip_id}")
