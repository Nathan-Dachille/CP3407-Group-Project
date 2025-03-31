from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.http import JsonResponse
from authuser.models import CleanerAvailability
from django.contrib.auth.decorators import login_required


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
