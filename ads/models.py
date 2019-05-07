from django.db import models
from django.contrib.auth import get_user_model


class Ads(models.Model):
    name = models.CharField('Название', max_length=250, default='Моя реклама')
    description = models.TextField('Описание', max_length=300, blank=True)
    preview = models.ImageField('Превью', blank=True)
    user = models.ForeignKey(get_user_model(), models.CASCADE)

    class Meta:
        verbose_name = 'Рекламная публикация'
        verbose_name_plural = 'Рекламные публикации'
