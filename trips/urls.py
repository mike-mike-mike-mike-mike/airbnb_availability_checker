from django.urls import path

from . import views

app_name = "trips"
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("create/", views.create, name="create"),
    path("<int:trip_id>/", views.show, name="show"),
    path("<int:trip_id>/edit/", views.edit, name="edit"),
]
