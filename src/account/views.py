from django.shortcuts import render

# Create your views here.
def account(request, *args, **kwargs):
    return render(request, "account.html", {})
