from rest_framework import generics, permissions
from ads.models import Advertisement, Comment
from ads.serializers import AdvertisementSerializer, CommentSerializer
from ads.permissions import IsAuthorOrAdmin
from rest_framework.exceptions import ValidationError


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


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     advertisement_id = self.kwargs.get("advertisement_id")
    #     if advertisement_id:
    #         serializer.save(author=self.request.user, advertisement_id=advertisement_id)
    #     else:
    #         serializer.save(author=self.request.user)

    def perform_create(self, serializer):
        advertisement_id = self.request.data.get("advertisement")
        if not advertisement_id:
            raise ValidationError({"advertisement": "Это поле обязательно."})
        try:
            advertisement = Advertisement.objects.get(pk=advertisement_id)
        except Advertisement.DoesNotExist:
            raise ValidationError({"advertisement": "Объявление не найдено."})
        serializer.save(author=self.request.user, advertisement=advertisement)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        advertisement_id = self.kwargs.get("advertisement_id")
        if advertisement_id:
            # получаем список комментариев для конкретного объявления
            return Comment.objects.filter(advertisement_id=advertisement_id)
        return Comment.objects.all()


class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]
