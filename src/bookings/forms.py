from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time', 'service', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),  # Start time field
            'end_time': forms.TimeInput(attrs={'type': 'time'}),  # End time field
            'notes': forms.Textarea(attrs={'placeholder': 'Enter your message here...', 'rows': 4}),
        }