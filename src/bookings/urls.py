from django.urls import path
from .views import book_appointment, booking_success

urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    path('success/', booking_success, name='booking_success'),
]