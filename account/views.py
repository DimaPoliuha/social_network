import os

import clearbit
import requests
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import SignupForm
from .tokens import account_activation_token


def get_clearbit_data(email):
    clearbit.key = os.getenv("CLEARBIT_API")
    response = clearbit.Enrichment.find(email=email, stream=True)
    name, surname = None, None
    if response is not None:
        name = response["person"]["name"]["givenName"]
        surname = response["person"]["name"]["familyName"]
    return name, surname


def emailhunter_check(email):
    api_key = os.getenv("EMAILHUNTER_API")
    req = {"api_key": api_key, "email": email}
    try:
        response = requests.get("https://api.hunter.io/v2/email-verifier", params=req)
    except requests.exceptions.RequestException:
        return False
    response_data = response.json()
    data = response_data["data"]
    if data["regexp"] and data["smtp_server"]:
        return True
    else:
        return False


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        email = request.POST.get("email")
        email_check = emailhunter_check(email)
        if form.is_valid() and email_check:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            if not first_name and not last_name:
                first_name, last_name = get_clearbit_data(email)
            elif not first_name and last_name:
                first_name, _ = get_clearbit_data(email)
            elif first_name and not last_name:
                _, last_name = get_clearbit_data(email)

            form_values = request.POST.copy()
            form_values["first_name"] = first_name
            form_values["last_name"] = last_name
            form = SignupForm(form_values)

            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your blog account."
            mail_context = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }
            message = render_to_string("account/email_activation.html", mail_context)
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(
                request,
                f"{user}, please confirm your email to complete the registration",
            )
            return redirect("blog:index")
        elif not email_check:
            messages.warning(request, f"Specify correct email!")
    else:
        form = SignupForm()
    return render(request, "account/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f"{user}, your email was confirmed successfully.")
        return redirect("blog:index")
    else:
        messages.warning(request, f"Activation link is invalid!")
        return redirect("blog:index")
