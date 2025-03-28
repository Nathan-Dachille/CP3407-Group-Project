"""
URL configuration for cleaning_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from pages.views import home
from authuser.views import sign_in_view, register_view, sign_out_view
from bookings.views import book_appointment
from account.views import account
from django.contrib.auth.views import PasswordChangeView

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('bookings/', book_appointment, name="book_appointment"),
    path('sign_in/', sign_in_view, name="sign_in"),
    path('register/', register_view, name="register"),
    path('sign_out/', sign_out_view, name="sign_out"),
    path('profile/', account, name='account'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('change-email/', CustomPasswordChangeView.as_view(), name='email_change')
]
