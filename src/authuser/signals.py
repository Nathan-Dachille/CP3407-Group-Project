# bookings/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from bookings.models import Booking
from authuser.models import User


@receiver(post_delete, sender=Booking)
def update_user_rating_on_delete(sender, instance, **kwargs):
    if instance.user:
        instance.user.update_rating(by_signal=True)
    if instance.assigned:
        instance.assigned.update_rating(by_signal=True)


@receiver(post_save, sender=Booking)
def update_user_rating(sender, instance, created, **kwargs):
    if instance.user:
        instance.user.update_rating(by_signal=True)
    if instance.assigned:
        instance.assigned.update_rating(by_signal=True)


# For User model signals
@receiver(post_save, sender=User)
def update_user_rating_on_user_save(sender, instance, created, **kwargs):
    if instance.role in [User.Role.CUSTOMER, User.Role.CLEANER]:
        instance.update_rating(by_signal=True)