import datetime as dt

from django.test import TestCase

from authuser.models import User
from bookings.models import Booking


class BookingTests(TestCase):
    def setUp(self):
        print("Creating a user...")
        self.user = User.objects.create_user(
            username="TestUser2",
            email="thisis@test2.au",
            password="testpassword!",
            role="CUSTOMER",
            phone="+111111111",
            rating=1,
        )

        print("Creating a booking...")
        self.booking = Booking(
            user=self.user,
            date=dt.date(2024, 1, 1),
            start_time=dt.time(12),
            end_time=dt.time(16, 20),
            service="test",
        )
        pass

    def test_booking_string(self):
        print("Test booking string.")
        self.assertEqual(
            str(self.booking),
            "Booking by thisis@test2.au on 2024-01-01 from 12:00:00 to 16:20:00",
        )
