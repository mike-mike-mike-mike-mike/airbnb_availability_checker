from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse


from .models import Trip


def index(request):
    latest_trips = Trip.objects.order_by("-id")[:5]
    context = {
        "latest_trips": latest_trips,
    }

    return render(request, "trips/index.html", context)


def new(request, error_message=None):
    return render(request, "trips/new.html", {"error_message": error_message})


def create(request):
    # return HttpResponse("You're creating a new trip")
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


def show(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, "trips/show.html", {"trip": trip})


def edit(request, trip_id):
    return HttpResponse(f"You're editing trip {trip_id}")
