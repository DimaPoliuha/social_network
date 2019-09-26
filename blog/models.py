from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_title = models.CharField("post title", max_length=150)
    post_text = models.TextField("post text")
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
