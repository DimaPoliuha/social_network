import os

import requests
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

email_hunter_api_key = os.getenv("EMAILHUNTER_API")


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        unique_email = False
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            unique_email = True
        if not unique_email:
            raise forms.ValidationError("This email address is already in use.")

        req = {"api_key": email_hunter_api_key, "email": email}
        try:
            response = requests.get(
                "https://api.hunter.io/v2/email-verifier", params=req
            )
        except requests.exceptions.RequestException:
            raise forms.ValidationError("Bad response from hunter.io.")
        response_data = response.json()
        data = response_data["data"]
        if not data["regexp"] and not data["smtp_server"]:
            raise forms.ValidationError("Specify correct email!")
        return email
