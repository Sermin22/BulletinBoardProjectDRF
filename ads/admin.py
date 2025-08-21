from django.contrib import admin
from ads.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "description", "author", "created_at")
    list_filter = ("title", "author", "created_at")
    search_fields = ("title", "author")
