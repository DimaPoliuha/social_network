from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from account.forms import SignupForm, check_email_hunter
from account.tokens import account_activation_token
from account.views import get_clearbit_data
from blog.models import Like, Post

from .serializers import LikeSerializer, PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-pub_date")
    serializer_class = PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class SignupView(APIView):
    def post(self, request):
        form = SignupForm(data=request.data)
        email = request.data.get("email")
        email_verification = check_email_hunter(email)

        if form.is_valid() and email_verification is None:
            clear_first_name, clear_last_name = get_clearbit_data(email)

            form_values = request.data.copy()
            form_values["first_name"] = clear_first_name
            form_values["last_name"] = clear_last_name
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
            message = render_to_string(
                "account/rest_email_activation.html", mail_context
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "confirm your email to complete the registration",
                }
            )
        elif email_verification is not None:
            return Response(email_verification)
        return Response(form.errors)


def api_account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse(
            {"status": "success", "message": "your email was confirmed successfully"},
            status=200,
        )
    return JsonResponse({"status": "error", "message": "activation link invalid"})
