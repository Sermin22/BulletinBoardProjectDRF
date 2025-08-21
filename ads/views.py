from rest_framework import generics, permissions
from ads.models import Advertisement
from ads.serializers import AdvertisementSerializer
from ads.permissions import IsAuthorOrAdmin


class AdvertisementCreateView(generics.CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]  # Создавать могут только аутентифицированные пользователи

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdvertisementListView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    # permission_classes = [permissions.AllowAny]  # если в settings IsAuthenticated, список доступен всем


class AdvertisementDetailView(generics.RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]  # Просмотр только аутентифицированным пользователям


class AdvertisementUpdateView(generics.UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthorOrAdmin]  # Админ может изменять все, пользователь только свои


class AdvertisementDeleteView(generics.DestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthorOrAdmin]  # Админ может удалять все, пользователь только свои
