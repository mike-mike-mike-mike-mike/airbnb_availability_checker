from django.urls import path

from . import views

app_name = "trips"
urlpatterns = [
    path("", views.IndexView.as_view(), name="trip_list"),
    path("new/", views.CreateView.as_view(), name="new_trip"),
    path("<int:pk>/", views.DetailsView.as_view(), name="trip_details"),
    path("<int:pk>/edit/", views.UpdateView.as_view(), name="edit_trip"),
]
