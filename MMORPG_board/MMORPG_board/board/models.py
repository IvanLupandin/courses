from django.db import models
from django.contrib.auth.models import User
from .utils import send_newsletter
import json


class Advertisement(models.Model):
    CATEGORY_CHOICES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DPS', 'ДД'),
        ('Traders', 'Торговцы'),
        ('GuildMasters', 'Гилдмастеры'),
        ('QuestGivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Alchemists', 'Зельевары'),
        ('Enchanters', 'Мастера заклинаний'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Response(models.Model):
    text = models.TextField()
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(News, self).save(*args, **kwargs)
        send_newsletter(self.title, self.content)