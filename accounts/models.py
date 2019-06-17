from django.contrib.auth.models import AbstractUser
from django.db import models

from allauth.socialaccount.models import SocialAccount, SocialToken


class SmmUser(AbstractUser):

    """
    def find_avatar(self):
        if self.avatar:
            return self.avatar.url
        for social_account in self.socialaccount_set.all():
            if social_account.get_avatar_url():
                return social_account.get_avatar_url()
    """

    @property
    def has_social_profile(self):
        return SocialAccount.objects.filter(user=self).exists()

    @property
    def vk_social_account(self):
        if self.has_social_profile:
            return SocialAccount.objects.filter(user=self, provider='vk').first()

    @property
    def ok_social_account(self):
        if self.has_social_profile:
            return SocialAccount.objects.filter(user=self, provider='odnoklassniki').first()

    @property
    def facebook_social_account(self):
        if self.has_social_profile:
            return SocialAccount.objects.filter(user=self, provider='facebook').first()

    def get_facebook_token(self):
        account = self.facebook_social_account
        if account:
            tokens = SocialToken.objects.filter(account=account)
            if tokens.exists():
                return tokens.last().token

    def get_vk_token(self):
        account = self.vk_social_account
        if account:
            tokens = SocialToken.objects.filter(account=account)
            if tokens.exists():
                return tokens.last().token

    @property
    def has_aboutinfo(self):
        return hasattr(self, 'aboutinfo')

    # def get_absolute_url(self):
        # return reverse('get-userprofile', args=[self.pk])

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"