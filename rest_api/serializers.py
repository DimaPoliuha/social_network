from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Like, Post


class UserInfoSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    class Meta:
        model = User
        fields = ("url", "id", "username", "first_name", "last_name")


class PostInfoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:post-detail")
    author = UserInfoSerializer()

    class Meta:
        model = Post
        fields = ("url", "id", "post_title", "post_text", "author", "pub_date")


class LikeInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    post = PostInfoSerializer()

    class Meta:
        model = Like
        fields = ("post", "user")
