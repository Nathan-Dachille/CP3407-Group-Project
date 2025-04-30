import datetime as dt

from django.test import TestCase

from authuser.models import User
from bookings.models import Booking


class BookingTests(TestCase):
    @classmethod
    def setUpTestData(self):
        """Set up tests by creating user objects."""
        self.customer = User.objects.create_user(
            username="test_customer",
            email="test_customer@test.com",
            password="testpassword1",
            role="CUSTOMER",
            phone="+111111111",
            rating=1,
        )

        self.cleaner = User.objects.create_user(
            username="test_cleaner",
            email="test_cleaner@test.com",
            password="testpassword2",
            role="CLEANER",
            phone="+222222222",
            rating=1,
        )

        self.booking = Booking(
            user=self.customer,
            date=dt.date(2024, 1, 1),
            start_time=dt.time(12),
            end_time=dt.time(16, 20),
            service="test",
        )
        pass

    def test_booking_string(self):
        """Test the creation of a booking and its string method."""
        self.assertEqual(
            str(self.booking),
            "Booking by test_customer@test.com on 2024-01-01 from 12:00:00 to 16:20:00",
        )

    def test_booking_page_not_signed_in(self):
        """Test accessing booking page while not signed in."""
        response = self.client.get("/bookings", follow=True)
        self.assertRedirects(response, "/sign_in/?next=/bookings/", status_code=301)

    def test_booking_page_signed_in_cleaner(self):
        """Test accessing booking page while signed in as a customer."""
        self.client.login(username="test_cleaner", password="testpassword2")
        response = self.client.get("/bookings", follow=True)
        self.assertRedirects(response, "/profile/", status_code=301)

    def test_booking_page_signed_in_customer(self):
        """Test accessing booking page while signed in as a customer."""
        self.client.login(username="test_customer", password="testpassword1")
        response = self.client.get("/bookings", follow=True)
        self.assertTemplateUsed(response, "booking_form.html")
        self.assertTemplateUsed(response, "navbar.html")
