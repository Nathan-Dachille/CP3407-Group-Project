from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.core import serializers
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone
from authuser.models import CleanerAvailability
from bookings.models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from authuser.forms import EmailChangeForm
import json
import logging

logger = logging.getLogger(__name__)

"""
Primary Account View
"""


@login_required(login_url="/sign_in/")
def account(request, *args, **kwargs):
    # Get Date
    user_date_str = request.GET.get("user_date", None)
    if user_date_str:
        user_date = datetime.strptime(user_date_str, "%Y-%m-%d").date()
    else:
        user_date = datetime.today().date()  # Fallback to server date

    day_list, week_num = get_date_info(user_date)

    # Get Availability
    # Get all bookings for the logged-in user
    ava_data = list(CleanerAvailability.objects.filter(cleaner=request.user)
                    .values("date", "available_hours"))

    for item in ava_data:
        item["ava_date"] = item.pop("date").strftime("%Y-%m-%d")

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            "current_date": user_date,
            "week_number": week_num,
            "week_dates": day_list,
            "ava_data": ava_data,
        })
    return render(request, "account.html", {
        "current_date": user_date,
        "week_dates": day_list,
        "week_number": week_num,
        "ava_data": ava_data,
        'user_role': request.user.role,
    })


"""
Primary Account Functions
"""


@login_required
def update_user_info(request):
    if request.method == 'POST':
        # Get the user from the request
        user = request.user

        # Update the phone and address if the user provided new values
        if 'phone' in request.POST:
            user.phone = request.POST['phone']
        if 'address' in request.POST:
            user.address = request.POST['address']

        # Save the updated user information
        user.save()

        # Redirect back to the profile page or wherever you want
        return redirect('account')  # Make sure you have a 'profile' view and URL

    return redirect('account')  # In case it's not a POST request


"""
Password and email change views
"""


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"

    def get_success_url(self):
        # After successfully changing the password, redirect to the profile page
        return reverse_lazy('account')  # 'account' should match your profile URL name


@login_required(login_url="/sign_in/")
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            # Check password validity
            password = form.cleaned_data['password']
            new_email = form.cleaned_data['new_email']
            user = request.user
            correct_password = user.password

            match_check = check_password(password, correct_password)

            if match_check:
                user.email = new_email
                user.save()
                messages.success(request, "Your email has been successfully updated.")
                return redirect('account')  # Redirect to the profile page or another appropriate view
            else:
                messages.error(request, "Incorrect password.")
    else:
        form = EmailChangeForm()

    return render(request, 'account.html', {'form': form})


"""
Cleaner Requests, Functions, and Classes
"""


# Availability Requests and Classes


@login_required(login_url="/sign_in/")
def toggle_availability(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.debug(f"Received data: {data}")  # Debugging line

            user = request.user
            tog_type = data.get("type")
            dates = data.get("days", [])
            hours = data.get("hours", [])

            if not tog_type or not isinstance(dates, list) or not isinstance(hours, list):
                return JsonResponse({"success": False, "error": "Invalid data format"}, status=400)

            if tog_type == 1:
                a_hours = hours or list(range(24))  # Default to all hours if none provided

                # Fetch existing hours for the selected dates
                existing_hours = {
                    hour
                    for availability in CleanerAvailability.objects.filter(cleaner=user, date__in=dates)
                    for hour in availability.available_hours
                    if hour in a_hours
                }

                any_hours_exist = any(
                    CleanerAvailability.objects.filter(cleaner=user, date=date).exists() for date in dates)

                for date in dates:
                    availability, created = CleanerAvailability.objects.get_or_create(cleaner=user, date=date)
                    current_hours = set(availability.available_hours)

                    if not hours:  # Weekly or daily toggle
                        availability.available_hours = list(range(24)) if not any_hours_exist else []
                    else:  # Hourly toggle
                        availability.available_hours = [
                                                           hour for hour in current_hours if hour not in hours
                                                       ] + [hour for hour in hours if hour not in existing_hours]

                    # Save or delete based on availability
                    if availability.available_hours:
                        availability.save()
                    else:
                        availability.delete()

            elif tog_type == 2:
                for date in dates:
                    availability, created = CleanerAvailability.objects.get_or_create(cleaner=user, date=date)
                    if not hours:
                        hours = list(range(24))
                    for hour in hours:
                        if hour in availability.available_hours:
                            availability.available_hours.remove(hour)  # Remove the hour
                        else:
                            availability.available_hours.append(hour)  # Add the hour

                    # Save the updated availability (if it still has hours)
                    if availability.available_hours:
                        availability.save()
                    else:
                        availability.delete()  # If no hours are left, remove the entry
            else:
                return JsonResponse({"success": False, "error": "Invalid toggle type"}, status=400)

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


@login_required(login_url="/sign_in/")
def duplicate_availability(request):
    if request.method == "POST":
        data = json.loads(request.body)
        logger.debug(f"Received data: {data}")
        user = request.user
        target_date = datetime.strptime(data.get("t_date"), "%Y-%m-%d").date()
        week_dates = [datetime.strptime(date_str, "%Y-%m-%d").date() for date_str in data.get("s_week")]

        if not target_date:
            return JsonResponse({"success": False, "error": "Invalid target date."})
        if not week_dates:
            return JsonResponse({"success": False, "error": "Invalid week dates."})

        # Fetch the availability for the current week
        week_dates_start = week_dates[0]  # Assuming week_dates is a list with start and end date
        week_dates_end = week_dates[6]

        # Fetch availability data for the current week
        availability_records = CleanerAvailability.objects.filter(
            cleaner=user,
            date__range=[week_dates_start, week_dates_end],
        )

        # Initialize a dictionary to hold the availability for each weekday
        current_week_availability = {}
        for availability in availability_records:
            weekday = availability.date.weekday()
            if weekday not in current_week_availability:
                current_week_availability[weekday] = []
            current_week_availability[weekday].extend(availability.available_hours)

        date_range = get_date_range(week_dates[6], target_date)

        for date in date_range:
            # Get the available hours for the current date's weekday (if it exists)
            new_available_hours = current_week_availability.get(date.weekday(), [])

            # Fetch the existing availability for this date
            availability, created = CleanerAvailability.objects.get_or_create(
                cleaner=user,
                date=date,
            )

            # If there are available hours for this date, update them
            if new_available_hours:
                # Remove hours that are no longer available
                hours_to_remove = set(availability.available_hours) - set(new_available_hours)
                for hour in hours_to_remove:
                    availability.available_hours.remove(hour)

                # Add hours that are now available
                hours_to_add = set(new_available_hours) - set(availability.available_hours)
                for hour in hours_to_add:
                    availability.available_hours.append(hour)
            else:
                # If no available hours for this day, make it fully unavailable (empty list)
                availability.available_hours = []

            if availability.available_hours:
                availability.save()
            else:
                availability.delete()  # If no hours are left, remove the entry

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method."})


class AvailabilityWrapper(dict):
    @property
    def dates(self):
        return list(self.keys())


# Booking Requests and Functions


@login_required(login_url="/sign_in/")
def get_bookings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            dates = data.get("dates", [])
            user = request.user

            # Get all assigned bookings within the requested dates
            booking_data_a = list(Booking.objects.filter(assigned=user, date__in=dates))

            raw_availability = data.get("availability", [])

            availability = AvailabilityWrapper({
                entry["ava_date"]: entry["available_hours"]
                for entry in raw_availability
            })

            filtered_bookings_assigned = []

            # Iterate over each assigned booking and remove the available hours that are already booked
            for booking in booking_data_a:
                # Get the booking hours using the helper function
                booking_hours = get_booking_hours(booking)
                booking_date = booking.date.strftime("%Y-%m-%d")

                filtered_bookings_assigned.append({
                    "id": booking.id,
                    "date": booking_date,
                    "booking_hours": booking_hours
                })

                if booking_date in availability.dates:
                    # Get the available hours for this booking date
                    available_hours = availability[booking.date.strftime("%Y-%m-%d")]

                    # Remove the hours of the booking from the available hours
                    for hour in booking_hours:
                        if hour in available_hours:
                            available_hours.remove(hour)

                    # After modifying the available hours, update the availability dictionary
                    availability[booking.date.strftime("%Y-%m-%d")] = available_hours

            # Get all unassigned bookings within the requested dates
            booking_data_u = list(Booking.objects.filter(assigned__isnull=True, date__in=availability.dates))

            filtered_bookings_unassigned = []

            for booking in booking_data_u:
                booking_date = str(booking.date)  # Format to match availability keys

                # Skip if no availability data for this date
                if booking_date not in availability.dates:
                    continue

                # Check if the cleaner's suburb matches the customer's suburb (if both have addresses)
                cleaner_suburb = user.get_suburb() if user.get_suburb() else None
                customer_suburb = booking.user.get_suburb() if booking.user.get_suburb() else None

                if cleaner_suburb and customer_suburb and cleaner_suburb != customer_suburb:
                    continue  # Skip this booking if the suburbs don't match

                available_hours = availability[booking_date]

                booking_hours = get_booking_hours(booking)

                # Include booking only if all hours are available
                if all(hour in available_hours for hour in booking_hours):
                    filtered_bookings_unassigned.append({
                        "id": booking.id,
                        "date": booking_date,
                        "booking_hours": booking_hours
                    })

            return JsonResponse({
                "success": True,
                "bookings_u": filtered_bookings_unassigned,
                "bookings_a": filtered_bookings_assigned,
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


def find_booking(request):
    booking_id = request.GET.get("booking_id", None)
    if booking_id:
        booking = Booking.objects.select_related("user", "assigned").get(id=booking_id)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "bookingInfo": {
                    "id": booking.id,
                    "date": str(booking.date),
                    "start_time": booking.start_time.strftime("%H:%M"),
                    "end_time": booking.end_time.strftime("%H:%M") if booking.end_time else None,
                    "service": booking.service,
                    "notes": booking.notes,
                    "user_id": booking.user.id,
                    "user_name": booking.user.get_full_name() or booking.user.username,
                    "rating": booking.user.rating,
                    "email": booking.user.email,
                    "phone": booking.user.phone,
                    "address_str": None,
                    "assigned_id": booking.assigned.id if booking.assigned else None,
                }
            })
        return render(request, "account.html", {
            "bookingInfo": booking,
        })


@login_required(login_url="/sign_in/")
def toggle_accept(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            logger.debug(f"Received data: {data}")  # Debugging line
            booking_id = data.get("target")
            booking = Booking.objects.select_related("user", "assigned").get(id=booking_id)
            if booking.assigned is None:
                booking.assigned = user
            else:
                booking.assigned = None
            booking.save()

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


"""
Customer Requests, Functions, and Classes
"""


@login_required
def customer_bookings(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        now = timezone.now()
        bookings = Booking.objects.filter(user=request.user).order_by('-date')
        booking_data = [
            {
                "id": b.id,
                "date": b.date.isoformat(),
                "start_time": b.start_time.strftime("%H:%M"),
                "end_time": b.end_time.strftime("%H:%M") if b.end_time else None,
                "service": b.service,
                "notes": b.notes,
                "user_name": (
                    b.assigned.get_full_name() or b.assigned.username
                    if b.assigned else
                    None
                ),
                "rating": b.assigned.rating if b.assigned else None,
                "email": b.assigned.email if b.assigned else None,
                "phone": b.assigned.phone if b.assigned else None,
                "status": "Past" if (b.date < now.date() or (b.date == now.date() and b.start_time < now.time()))
                else "Upcoming"
            }
            for b in bookings
        ]
        return JsonResponse({"bookings": booking_data})


"""
General Functions
"""


@login_required(login_url="/sign_in/")
def delete_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.debug(f"Received data: {data}")  # Debugging line
            booking_id = data.get("target")
            booking = Booking.objects.select_related("user", "assigned").get(id=booking_id)
            booking.delete()

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


@login_required(login_url="/sign_in/")
def set_booking_rating(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("id")
            rating = data.get("rating")
            source = data.get("source")

            booking = Booking.objects.get(id=booking_id)

            if source == 1:
                booking.cleaner_rating = rating
            elif source == 2:
                booking.customer_rating = rating
            else:
                return JsonResponse({"error": "Invalid source."}, status=400)

            booking.save()
            return JsonResponse({"success": True})

        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_date_range(start_date, end_date):
    """
    Returns a list of dates from start_date to end_date (inclusive).
    Assumes start_date and end_date are datetime objects.
    """
    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date)  # Add the date part only
        current_date += timedelta(days=1)  # Move to the next day

    return date_list


def get_date_info(date):
    week_start = date - timedelta(days=date.weekday())  # Monday
    # Generate a list of all dates in the week (Monday to Sunday)
    week_dates = [(week_start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    week_num = date.isocalendar().week

    return week_dates, week_num


def get_booking_hours(booking):
    """
    Get the list of hours for a booking, from start time to end time.
    If end_time is None, return only the start hour.
    """
    start_hour = booking.start_time.hour
    booking_hours = []

    if booking.end_time is None:
        # If end_time is null, return only the start hour
        booking_hours = [start_hour]
    else:
        end_hour = booking.end_time.hour

        # Round down end_time if it has minutes
        if booking.end_time.minute > 0:
            end_hour += 1

        # If the start hour is the same as the end hour, return that one hour
        if start_hour == end_hour:
            booking_hours = [start_hour]
        else:
            # Otherwise, return all hours between start and end, excluding the end hour
            booking_hours = list(range(start_hour, end_hour))

    return booking_hours
