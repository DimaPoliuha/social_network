import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField("user name", max_length=60)
    surname = models.CharField("user surname", max_length=60)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField("post title", max_length=150)
    post_text = models.TextField("post text")
    pub_date = models.DateTimeField("date published")
    likes_count = models.IntegerField("likes count", default=0)

    def __str__(self):
        return self.post_title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.pub_date <= now
