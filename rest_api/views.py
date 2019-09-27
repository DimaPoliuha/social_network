from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.forms import SignupForm
from account.tokens import account_activation_token
from account.views import get_clearbit_data
from blog.models import Like, Post

from . import serializers
from .forms import LikeForm, PostForm


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
    return JsonResponse(
        {"status": "error", "message": "activation link invalid"}, status=410
    )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-pub_date")
    serializer_class = serializers.PostInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserInfoSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeInfoSerializer


class SignupView(APIView):
    def post(self, request):
        form = SignupForm(data=request.data)
        email = request.data.get("email")

        if form.is_valid():
            clear_first_name, clear_last_name = get_clearbit_data(email)

            form_values = request.data.copy()
            form_values["first_name"] = clear_first_name
            form_values["last_name"] = clear_last_name
            form = SignupForm(form_values)

            user = form.save(commit=False)
            user.is_active = True
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
                },
                status=200,
            )
        return Response(form.errors, status=409)


class PostCreationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        post_values = request.data.copy()
        user = User.objects.get(username=post_values["author"])
        post_values["author"] = str(user.id)
        form = PostForm(post_values)

        if form.is_valid():
            form.save()
            return Response(form.data, status=200)
        return Response(form.errors, status=409)


class LikeCreationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        post_values = request.data.copy()
        user = User.objects.get(username=post_values["user"])
        new_like, created = Like.objects.get_or_create(
            user_id=user.id, post_id=post_values["post_id"]
        )
        if not created:
            new_like.delete()
            return JsonResponse(
                {"status": "success", "message": "disliked"}, status=200
            )
        return JsonResponse({"status": "success", "message": "liked"}, status=200)
