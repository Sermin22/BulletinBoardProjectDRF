from rest_framework import serializers
from ads.models import Advertisement, Comment
from users.serializers import CustomUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    # при создании можно указать id объявления, если путь общий (/comments/create/)
    advertisement = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all(),
        required=False  # делаем необязательным, т.к. можем взять из URL
    )

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "advertisement", "created_at"]


class AdvertisementSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ["id", "title", "price", "description", "image", "author", "created_at", "comments"]
