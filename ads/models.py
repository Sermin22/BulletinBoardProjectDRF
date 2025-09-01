from django.db import models
from config import settings


class Advertisement(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    price = models.PositiveIntegerField(verbose_name="Цена товара")
    description = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(upload_to="ads/product_photo/", verbose_name="Фото товара", blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="advertisements",
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["-created_at"]  # сортировка по убыванию даты
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f"{self.title} ({self.price}₽)"


class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария"
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Объявление"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий {self.text} от {self.author} к {self.advertisement}"
