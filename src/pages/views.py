from django.shortcuts import render


# Create your views here.


def home(request, *args, **kwargs):
    confirmed = request.GET["confirmed"] == "True"
    return render(request, "home.html", {"confirmed": confirmed})
