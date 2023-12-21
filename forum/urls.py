from django.urls import path

from .views import (AboutUsView, NewsDetailView, NewsListView, PostCreateView,
                    PostDeleteView, PostDetailView, PostListView,
                    PostUpdateView, CommentUpdateView, CommentDeleteView)

urlpatterns = [
    path("", PostListView.as_view(), name="posts"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    path("news/", NewsListView.as_view(), name="news"),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
