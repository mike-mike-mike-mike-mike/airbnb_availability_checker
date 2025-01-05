from django.test import TestCase
from django.urls import reverse
from trips.models import Trip, RoomDetail
from users.models import User


class TripModelTests(TestCase):
    def create_trip(self, room_id="123", check_in="2021-01-01", check_out="2021-01-02"):
        user = User(username="test_user")
        user.save()
        return Trip.objects.create(
            room_id=room_id, check_in=check_in, check_out=check_out, user=user
        )

    def test_trip_id(self):
        trip = self.create_trip()
        self.assertEqual(trip.trip_id, "123_2021-01-01_2021-01-02")

    def test_str(self):
        trip = self.create_trip()
        self.assertEqual(
            str(trip),
            (
                f"Trip(id: {trip.id}, room_id: 123, check_in: 2021-01-01, check_out: 2021-01-02, "
                f"available: False, user: {trip.user})"
            ),
        )


class RoomDetailModelTests(TestCase):
    def test_str__short_name(self):
        room_detail = RoomDetail(room_id="123", display_name="short name")
        self.assertEqual(
            str(room_detail), "RoomDetail(room_id: 123, display_name: short name)"
        )

    def test_str__long_name(self):
        room_detail = RoomDetail(
            room_id="123", display_name="a very long name that is over 32 characters"
        )
        self.assertEqual(
            str(room_detail),
            "RoomDetail(room_id: 123, display_name: a very long name that is over 32...)",
        )


class TripListViewTests(TestCase):
    def test_no_trips(self):
        """
        If no trips exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("trips:trip_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No saved trips.")
        self.assertQuerySetEqual(response.context["trip_list"], [])
