from django.contrib.auth.models import User
from rest_framework import viewsets

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
