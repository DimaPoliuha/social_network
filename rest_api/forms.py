from django import forms

from blog.models import Like, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("author", "post_text", "post_title")


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ("user", "post")
