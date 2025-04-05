from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from django.http import JsonResponse
from authuser.models import CleanerAvailability
from bookings.models import Booking
from django.contrib.auth.decorators import login_required
import json
import logging

logger = logging.getLogger(__name__)


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


class AvailabilityWrapper(dict):
    @property
    def dates(self):
        return list(self.keys())


def get_date_info(date):
    week_start = date - timedelta(days=date.weekday())  # Monday
    # Generate a list of all dates in the week (Monday to Sunday)
    week_dates = [(week_start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    week_num = date.isocalendar().week

    return week_dates, week_num


# Create your views here.
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
    })


@login_required(login_url="/sign_in/")
def get_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            dates = data.get("dates", [])
            print(dates)
            raw_availability = data.get("availability", [])
            availability = AvailabilityWrapper({
                entry["ava_date"]: entry["available_hours"]
                for entry in raw_availability
            })
            print(availability.dates)

            # Get all unassigned bookings within the requested dates
            booking_data = list(Booking.objects.filter(assigned__isnull=True, date__in=dates))
            print(booking_data)

            filtered_bookings = []

            for booking in booking_data:
                print(booking.date)
                booking_date = str(booking.date)  # Format to match availability keys

                # Skip if no availability data for this date
                if booking_date not in availability.dates:
                    print("error")
                    continue

                available_hours = availability[booking_date]
                print(available_hours)

                # Get integer hours from booking start to end
                print(booking.start_time)
                start_hour = booking.start_time.hour
                print(start_hour)

                # If end_time is null, return only the start hour
                if booking.end_time is None:
                    booking_hours = [start_hour]
                else:
                    print(booking.end_time)
                    end_hour = booking.end_time.hour
                    print(end_hour)

                    # Round down end_time if it has minutes
                    if booking.end_time.minute > 0:
                        end_hour += 1
                        print(end_hour)

                    # If the start hour is the same as the end hour, return that one hour
                    if start_hour == end_hour:
                        booking_hours = [start_hour]
                    else:
                        # Otherwise, return all hours between start and end, excluding the end hour
                        booking_hours = list(range(start_hour, end_hour))

                print(booking_hours)

                # Include booking only if all hours are available
                if all(hour in available_hours for hour in booking_hours):
                    filtered_bookings.append({
                        "id": booking.id,
                        "date": booking_date,
                        "booking_hours": booking_hours
                    })

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        "booking_data": filtered_bookings,
                    })
                return render(request, "account.html", {
                    "booking_data": filtered_bookings,
                })

            return JsonResponse({
                "success": True,
                "bookings": filtered_bookings
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


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