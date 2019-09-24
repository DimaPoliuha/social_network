from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Post


class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "latest_posts_list"

    def get_queryset(self):
        """
        Return the last five published posts (not including those set to be
        published in the future).
        """
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Post
    template_name = "blog/detail.html"


def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.likes_count += 1
    post.save()
    return HttpResponseRedirect(reverse("blog:detail", args=(post.id,)))
