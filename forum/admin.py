from django.contrib import admin

from .models import AboutUs, Comment, News, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "author"]
    list_display_links = ["id", "title"]
    list_filter = [
        "created_at",
    ]
    fields = ["title", "image", "text", "author"]
    ordering = [
        "created_at",
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "created_at", "post", "author"]
    list_display_links = ["id", "text"]
    list_filter = ["post", "author", "created_at"]
    fields = ["text", "created_at"]
    ordering = ["created_at", "post"]
    readonly_fields = ["created_at", "author", "post"]


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    fields = ["title", "text"]

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        if self.model.objects.count() < 1:
            return super().add_view(request, extra_context)
        else:
            object = (self.model.objects.first()).id
            return super().change_view(
                request=request, extra_context=extra_context, object_id=str(object)
            )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ["title", "image", "text", "created_at"]
    list_display = ["id", "title", "created_at"]
    list_display_links = ["id", "title"]
    readonly_fields = [
        "created_at",
    ]
    list_filter = [
        "created_at",
    ]
    ordering = [
        "-created_at",
    ]
