from django.test import TestCase
from authuser.models import User


class ProfilePageReponseTest(TestCase):
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
        pass

    def test_profile_page_not_signed_in(self):
        """Test accessing profile page while not signed in."""
        response = self.client.get("/profile", follow=True)
        self.assertRedirects(response, "/sign_in/?next=/profile/", status_code=301)

    def test_profile_page_signed_in(self):
        """Test accessing profile page while signed in."""
        self.client.login(username="test_customer", password="testpassword1")
        response = self.client.get("/profile", follow=True)
        self.assertTemplateUsed(response, "account.html")
        self.assertTemplateUsed(response, "navbar.html")
