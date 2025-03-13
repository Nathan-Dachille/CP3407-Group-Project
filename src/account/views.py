from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/sign_in/")
def account(request, *args, **kwargs):
    return render(request, "account.html", {})
