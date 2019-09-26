from django.contrib.auth.models import User
from rest_framework import viewsets

from blog.models import Post

from .serializers import PostSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-pub_date")
    serializer_class = PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
