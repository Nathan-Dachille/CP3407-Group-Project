from django.db import models
from authuser.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()  # Start time for booking
    end_time = models.TimeField(null=True, blank=True)  # Optional end time
    service = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.email} on {self.date} from {self.start_time} to {self.end_time or 'N/A'}"
