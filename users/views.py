from rest_framework.generics import CreateAPIView
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status, generics
from users.serializers import ResetPasswordSerializer, ResetPasswordConfirmSerializer
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreateAPIView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    # permission_classes = [AllowAny]  # если в settings.py настройка IsAuthenticated

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            subject="Сброс пароля",
            message=f"Для сброса пароля перейдите по ссылке: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({"detail": "Ссылка для сброса отправлена на почту"}, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
