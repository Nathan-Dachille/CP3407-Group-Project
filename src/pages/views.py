from django.shortcuts import render


# Create your views here.


def home(request, *args, **kwargs):
    confirmed = True if "confirmed" in request.GET else False
    return render(request, "home.html", {"confirmed": confirmed})
