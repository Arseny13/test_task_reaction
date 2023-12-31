# Generated by Django 4.2.5 on 2023-11-08 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Имя записи')),
                ('text', models.TextField(max_length=100, verbose_name='Текст')),
                ('create_date', models.DateField(
                    auto_now_add=True, verbose_name='Дата заказа')),
                ('publish', models.BooleanField(default=False,
                 verbose_name='Опубликована ли запись')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
