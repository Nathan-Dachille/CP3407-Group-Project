from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from authuser.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name', 'role', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email  {email} is already in use.")


class SignInForm(AuthenticationForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password')
