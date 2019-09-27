import os

import requests
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from blog.models import Like, Post

email_hunter_api_key = os.getenv("EMAILHUNTER_API")


def check_email_unique(email):
    unique_email = False
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        unique_email = True
    if not unique_email:
        return "This email address is already in use."


def check_email_hunter(email):
    unique = check_email_unique(email)
    if unique is not None:
        return unique

    req = {"api_key": email_hunter_api_key, "email": email}
    try:
        response = requests.get("https://api.hunter.io/v2/email-verifier", params=req)
    except requests.exceptions.RequestException:
        return "Bad response from hunter.io."
    response_data = response.json()
    data = response_data["data"]
    if not data["regexp"] or not data["smtp_server"]:
        return "Specify correct email!"
    return None


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")
    first_name = forms.CharField(
        max_length=150, required=False, widget=forms.HiddenInput()
    )
    last_name = forms.CharField(
        max_length=150, required=False, widget=forms.HiddenInput()
    )

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
        check_email_response = check_email_hunter(email)
        if check_email_response is not None:
            raise forms.ValidationError(check_email_response)
        return email


# class PostForm(forms.ModelForm):
#     post_text = forms.CharField(max_length=200)
#     class Meta:
#         model = Post
#         fields = ('user', 'post_text')
