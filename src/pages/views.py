from django.shortcuts import render


# Create your views here.

def home(request, *args, **kwargs):
    return render(request, "home.html", {})


def sign_in(request, *args, **kwargs):
    return render(request, "sign_in.html", {})
