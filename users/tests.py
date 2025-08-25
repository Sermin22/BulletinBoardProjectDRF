from django.core import mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


User = get_user_model()


class ResetPasswordTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@mail.ru",
            username="testuser",
            password="old_password123"
        )

    def test_reset_password_request_sends_email(self):
        """Проверяем, что запрос на сброс пароля отправляет письмо"""
        url = reverse("users:reset_password")
        response = self.client.post(url, {"email": self.user.email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)  # проверяем, что письмо ушло
        self.assertIn("Для сброса пароля перейдите по ссылке", mail.outbox[0].body)

    def test_reset_password_confirm_changes_password(self):
        """Проверяем, что сброс реально меняет пароль"""
        # генерируем uid и token, как в вьюхе
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        url = reverse("users:reset_password_confirm")
        data = {
            "uid": uid,
            "token": token,
            "new_password": "new_password123"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверяем, что пароль изменился
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password123"))

    def test_reset_password_confirm_invalid_token(self):
        """Проверяем поведение при неверном токене"""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_token = "abc123"

        url = reverse("users:reset_password_confirm")
        data = {
            "uid": uid,
            "token": invalid_token,
            "new_password": "new_password123"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
