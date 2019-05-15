from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Ads(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    name = models.CharField('Название', max_length=250, default='Моя реклама')
    description = models.TextField('Описание', max_length=300, blank=True)
    preview = models.ImageField('Превью')
    link = models.URLField(verbose_name='Ссылка', default='https://facebook.com/me')
    campaign = models.ForeignKey('Campaign', blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    facebook_url = models.URLField(blank=True)
    vk_url = models.URLField(blank=True)

    def facebook_loaded(self):
        if self.facebook_url:
            return True

    def vk_loaded(self):
        if self.vk_url:
            return True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('get-ads', args=[self.id])

    class Meta:
        verbose_name = 'Рекламная публикация'
        verbose_name_plural = 'Рекламные публикации'


class Campaign(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    vk_id = models.PositiveIntegerField(blank=True, null=True)
    facebook_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField('Наименование', max_length=300)

    def has_vk(self):
        if self.vk_id is not None:
            return True

    def has_facebook(self):
        if self.facebook_id is not None:
            return True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рекламная кампания'
        verbose_name_plural = 'Рекламные кампании'
