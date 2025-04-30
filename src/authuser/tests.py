from django.core.exceptions import ValidationError
from django.test import TestCase

from authuser.models import User


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(self):
        """Set up tests by creating user object."""
        self.user = User.objects.create_user(
            username="TestUser",
            email="thisis@test.au",
            password="testpassword!",
            role="CUSTOMER",
            phone="+111111111",
            rating=1,
        )
        pass

    def test_phone_validation(self):
        """Test phone number validation."""
        self.user.phone = "NotAPhoneNumber"
        self.assertRaises(ValidationError, self.user.full_clean)


class AuthenticationPageTests(TestCase):
    def test_sign_in_page(self):
        """Test accessing sign in page."""
        response = self.client.get("/sign_in", follow=True)
        self.assertTemplateUsed(response, "sign_in.html")
        self.assertTemplateUsed(response, "navbar.html")

    def test_register_page(self):
        """Test accessing register page."""
        response = self.client.get("/register", follow=True)
        self.assertTemplateUsed(response, "register.html")
        self.assertTemplateUsed(response, "navbar.html")
