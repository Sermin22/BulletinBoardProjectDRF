from rest_framework import serializers
from ads.models import Advertisement
from users.serializers import CustomUserSerializer


class AdvertisementSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    class Meta:
        model = Advertisement
        fields = "__all__"
