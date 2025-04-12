from django.shortcuts import render, redirect
from .forms import BookingForm
from django.contrib.auth.decorators import login_required


@login_required(login_url="/sign_in/")
def book_appointment(request):

    # Check to see if user is a cleaner. Redirect to calendar.
    user_role = request.user.role
    if user_role == "CLEANER":
        return redirect("/profile")

    # User is a customer. Proceed to bookings.
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect("/?confirmed")
    else:
        form = BookingForm()

    return render(request, "booking_form.html", {"form": form})
