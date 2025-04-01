from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.http import JsonResponse
from authuser.models import CleanerAvailability
from django.contrib.auth.decorators import login_required
import json
import logging

logger = logging.getLogger(__name__)


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
