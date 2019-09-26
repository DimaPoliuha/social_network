from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Post


@receiver(post_save, sender=User)
def create_post(sender, instance, created, **kwargs):
    if created:
        post = Post.objects.create(
            author=instance,
            post_title="Welcome new member",
            post_text=f"Hi, I'm {instance}",
        )
        post.save()
