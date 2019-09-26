from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Like, Post


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "latest_posts_list"
    ordering = ["-pub_date"]
    paginate_by = 10


class UserPostListView(generic.ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-pub_date")


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["object"]
        likes_count = post.like_set.count()
        if self.request.user.is_authenticated:
            user_likes_this = (
                True if post.like_set.filter(user=self.request.user) else False
            )
        else:
            user_likes_this = False

        context["likes_count"] = likes_count
        context["user_likes_this"] = user_likes_this
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["post_title", "post_text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ["post_title", "post_text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("blog:index")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def like(request, post_id):
    new_like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
    if not created:
        new_like.delete()
    return HttpResponseRedirect(reverse("blog:detail", args=(post_id,)))
