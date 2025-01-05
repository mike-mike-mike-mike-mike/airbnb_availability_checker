from django.urls import path

from . import views

app_name = "trips"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("new/", views.new, name="new"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.DetailsView.as_view(), name="details"),
    path("<int:trip_id>/edit/", views.edit, name="edit"),
]
