from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER = "user"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
    ]

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="Роль пользователя")
    image = models.ImageField(upload_to="users/avatars/", verbose_name="Аватарка", blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
