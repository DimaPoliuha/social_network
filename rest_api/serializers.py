from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Like, Post


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    class Meta:
        model = User
        fields = ("url", "id", "username", "first_name", "last_name")


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.is_staff = True
            user.save()
        return user


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:post-detail")
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ("url", "id", "post_title", "post_text", "author", "pub_date")


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ("post", "user")
