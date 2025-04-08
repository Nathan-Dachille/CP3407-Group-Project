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
from django.urls import reverse, path
from pages.views import home
from authuser.views import sign_in_view, register_view, sign_out_view
from bookings.views import book_appointment
from account.views import (account, CustomPasswordChangeView, change_email, update_user_info, toggle_availability,
                           duplicate_availability, get_bookings, find_booking, toggle_accept, customer_bookings,
                           delete_booking, set_booking_rating)
from django.contrib.auth.views import PasswordChangeDoneView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('bookings/', book_appointment, name="book_appointment"),
    path('sign_in/', sign_in_view, name="sign_in"),
    path('register/', register_view, name="register"),
    path('sign_out/', sign_out_view, name="sign_out"),
    path('profile/', account, name='account'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('change-email/', change_email, name='email_change'),
    path('update_user_info/', update_user_info, name='update_user_info'),
    path("toggle_availability/", toggle_availability, name="toggle_availability"),
    path("duplicate_availability/", duplicate_availability, name="duplicate_availability"),
    path("get_bookings/", get_bookings, name="get_bookings"),
    path("find_booking/", find_booking, name="find_booking"),
    path("toggle_accept/", toggle_accept, name="toggle_accept"),
    path('api/customer_bookings/', customer_bookings, name='customer_bookings'),
    path('delete_booking/', delete_booking, name='delete_booking'),
    path('set_booking_rating/', set_booking_rating, name='set_booking_rating'),
]
