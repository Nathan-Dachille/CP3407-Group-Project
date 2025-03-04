from django import forms


class SignIn(forms.Form):
    username = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Password", max_length=100)
