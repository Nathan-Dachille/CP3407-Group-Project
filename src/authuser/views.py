from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from authuser.forms import RegistrationForm


# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/sign_in/")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


def sign_in_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "sign_in.html", {"form": form})


def sign_out_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")
