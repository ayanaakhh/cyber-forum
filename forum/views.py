from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from forum.forms import CommentForm
from forum.models import AboutUs, Comment, News, Post

User = get_user_model()


class PostListView(generic.ListView):
    model = Post
    template_name = "main_page.html"
    context_object_name = "posts"


class PostDetailView(View):
    template_name = "post_detail.html"

    def get(self, request, **kwargs):
        post = self.get_object()
        comment_form = CommentForm()
        comments = Comment.objects.filter(post=post)

        context = {
            "post": post,
            "comment_form": comment_form,
            "comments": comments,
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        else:
            comments = Comment.objects.filter(post=post)
            context = {
                "post": post,
                "comment_form": form,
                "comments": comments,
            }
            return render(request, self.template_name, context)

        return self.get(request, **kwargs)

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs["pk"])


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ["title", "image", "text"]
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = "post_update.html"
    fields = ["title", "image", "text"]
    success_url = reverse_lazy("posts")

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs["pk"], author=self.request.user)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts")

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs["pk"], author=self.request.user)


class AboutUsView(generic.ListView):
    model = AboutUs
    queryset = AboutUs.objects.all()
    template_name = "about_us.html"
    context_object_name = "objects"


class NewsListView(generic.ListView):
    model = News
    template_name = "news.html"
    context_object_name = "news"


class NewsDetailView(generic.DetailView):
    model = News
    template_name = "news_detail.html"
    context_object_name = "news"


class CommentUpdateView(LoginRequiredMixin, View):
    template_name = "comment_update.html"

    def get(self, request, pk):
        comment = self.get_object(pk)
        form = CommentForm(instance=comment)
        return render(request, self.template_name, {'form': form, 'comment': comment})

    def post(self, request, pk):
        comment = self.get_object(pk)
        form = CommentForm(request.POST, instance=comment)
        post_pk = comment.post.pk
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post_pk)
        return render(request, self.template_name, {'form': form, 'comment': comment})

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404


class CommentDeleteView(LoginRequiredMixin, View):
    template_name = "comment_confirm_delete.html"

    def get(self, request, pk):
        comment = self.get_object(pk)
        return render(request, self.template_name, {'comment': comment})

    def post(self, request, pk):
        comment = self.get_object(pk)
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404
