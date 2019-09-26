from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Like, Post


class LikeSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "is_superuser")


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    class Meta:
        model = User
        fields = ("url", "username", "first_name", "last_name", "is_superuser")


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ("post_title", "post_text", "author", "pub_date")
