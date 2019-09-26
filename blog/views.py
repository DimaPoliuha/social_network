from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Like, Post


class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "latest_posts_list"

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes_count = post.like_set.count()
    if request.user.is_authenticated:
        user_likes_this = True if post.like_set.filter(user=request.user) else False
    else:
        user_likes_this = False
    context = {
        "likes_count": likes_count,
        "post": post,
        "user_likes_this": user_likes_this,
    }
    return render(request, "blog/detail.html", context)


def like(request, post_id):
    new_like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
    if not created:
        new_like.delete()
    return HttpResponseRedirect(reverse("blog:detail", args=(post_id,)))
