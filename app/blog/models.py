from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Blog(models.Model):
    """Класс блога"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='blogs'
    )
    name = models.CharField(
        'Имя записи',
        max_length=20
    )
    text = models.TextField(
        'Текст',
        max_length=100
    )
    create_date = models.DateField(
        verbose_name='Дата заказа',
        auto_now_add=True
    )
    publish = models.BooleanField(
        'Опубликована ли запись',
        default=False
    )
