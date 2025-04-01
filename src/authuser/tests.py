from django.core.exceptions import ValidationError
from django.test import TestCase

from authuser.models import User


class UserModelTests(TestCase):
    def setUp(self):
        print("Creating a user...")
        self.user = User.objects.create_user(
            username="TestUser",
            email="thisis@test.au",
            password="testpassword!",
            role="CUSTOMER",
            phone="+111111111",
            rating=1,
        )
        pass

    # def test_user_role(self):
    # """Currently no role validation."""
    #     print("Test setting user role.")
    #     self.assertFieldOutput(
    #         self.user.role, {"Customer": "CUSTOMER", "Cleaner": "CLEANER"},
    #         {}
    #     )

    def test_phone(self):
        print("Test phone number validation.")
        self.user.phone = "NotAPhoneNumber"
        self.assertRaises(ValidationError, self.user.full_clean)
