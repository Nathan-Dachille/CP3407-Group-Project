from django.db import models
from authuser.models import User
from django.utils import timezone


class BookingQuerySet(models.QuerySet):
    def validate_and_clean(self):
        for booking in self:
            booking.delete_if_old_and_unassigned()
        return self


class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db).validate_and_clean()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()  # Start time for booking
    end_time = models.TimeField(null=True, blank=True)  # Optional end time
    service = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned = models.ForeignKey(User, related_name='assigned_bookings', blank=True, null=True, on_delete=models.SET_NULL)
    cleaner_rating = models.IntegerField(null=True)
    customer_rating = models.IntegerField(null=True)

    objects = BookingManager()  # Attach your manager here

    def should_be_deleted(self):
        # Check if the booking is unassigned and old
        now = timezone.now()
        if self.assigned is None and self.date < now.date():
            if self.date == now.date() and self.start_time < now.time():
                return True
            elif self.date < now.date():
                return True
        return False

    def delete_if_old_and_unassigned(self):
        if self.should_be_deleted():
            self.delete()

    def __str__(self):
        return f"Booking by {self.user.email} on {self.date} from {self.start_time} to {self.end_time or 'N/A'}"
