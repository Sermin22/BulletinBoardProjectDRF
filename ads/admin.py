from django.contrib import admin
from ads.models import Advertisement, Comment


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "description", "author", "created_at")
    list_filter = ("title", "author", "created_at")
    search_fields = ("title", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "author_id", "author", "advertisement_id", "advertisement", "created_at")
    list_filter = ("text", "author", "created_at")
    search_fields = ("text", "author")
