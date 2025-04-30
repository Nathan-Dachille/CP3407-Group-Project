from django.test import TestCase
from authuser.models import User


class PagesTest(TestCase):
    @classmethod
    def setUpTestData(self):
        """Set up tests by creating user object."""
        self.customer = User.objects.create_user(
            username="test_customer",
            email="test_customer@test.com",
            password="testpassword1",
            role="CUSTOMER",
            phone="+111111111",
            rating=1,
        )
        pass

    def test_home_page_not_signed_in(self):
        """Test accessing home page while not signed in."""
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "navbar.html")

    def test_home_page_signed_in(self):
        """Test accessing home page while signed in."""
        self.client.login(username="test_customer", password="testpassword1")
        response = self.client.get("/", follow=True)
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "navbar.html")

    def test_404_page(self):
        """Test 404 page redirect."""
        response = self.client.get("/arandomURL", follow=True)
        self.assertTemplateUsed(response, "404.html")
        self.assertTemplateUsed(response, "navbar.html")
