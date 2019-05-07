from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy

from allauth.socialaccount.models import SocialToken

from ads import forms
from ads.api.vk import add_ads


class CreateAdsView(FormView):
    form_class = forms.AdsCreateForm
    template_name = 'create_ads.html'
    success_url = '/'

    def form_valid(self, form):
        f = form.save(commit=False)
        vk_account = self.request.user.vk_social_account
        if vk_account:
            tokens = SocialToken.objects.filter(account=vk_account)
            add_ads(tokens.first().token, form['name'], form['description'])
        f.user = self.request.user
        f.save()
        return super().form_valid(form)
