from facebook_business.exceptions import FacebookRequestError
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import FormView, View, DetailView
from django.urls import reverse_lazy

from allauth.socialaccount.models import SocialToken

from ads import forms
from ads.api.vk import VkAds
from ads.api.facebook import FacebookAds
from ads.api.facebook_user import FacebookUser

from .models import Ads


class CreateAdsView(FormView):
    object = None
    form_class = forms.AdsCreateForm
    template_name = 'create_ads.html'
    success_url = '/'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        f.save()
        self.object = f
        return super().form_valid(form)


class AdsDetail(DetailView):
    model = Ads
    template_name = 'detail_ads.html'


class CreateAdsFacebook(View):

    def get(self, request, ads_id, *args, **kwargs):
        """
        Возращает конфигурацию для создания рекламы в виде JSON
        """
        configuration = dict()
        user = request.user
        token = user.get_facebook_token()
        if token is None:
            return HttpResponseBadRequest(content='Token not found')
        pages = FacebookUser(token).get_pages()
        configuration['pages'] = pages
        return JsonResponse(data=configuration)

    def post(self, request, ads_id):
        ads = get_object_or_404(Ads, id=ads_id)
        try:
            self.create_ads_facebook(ads, request.POST)
        except FacebookRequestError as error:
            return JsonResponse(status=400, data=error._error)
        return JsonResponse(status=200, data={})

    def create_ads_facebook(self, ads, configuration):
        """
        Получает последний access token у юзера из request,
        создает кампанию(либо достает из базы, уже существующую)
        к создайнной/найденой компании привязывает объявление

        :param form: форма с commit=False
        :return: None
        """
        token = self.request.user.get_facebook_token()
        if token:
            fb = FacebookAds(token)
            campaign = fb.get_or_create_campaign(
                user=self.request.user,
                name='Smm Tools Campaign',
            )
            image = fb.upload_image(ads.preview)
            ad_creative = fb.create_adcreative(ads.name, ads.description, configuration['page'], image['hash'], ads.link)
            fb.add_ads(
                campaign_id=campaign.facebook_id,
                creative_id=ad_creative['id'],
                name=ads.name
            )


class CreateAdsVk(View):

    def post(self, request, ads_id):
        ads = get_object_or_404(Ads, id=ads_id)
        data = self.create_ads_vk(ads)
        if data and data.get('error', None):
            return JsonResponse(status=400, data=data)
        return JsonResponse(status=200, data={})

    def create_ads_vk(self, ads):
        """
        Аналогичная логика как в методе с facebook
        """
        token = self.request.user.get_vk_token()
        if token:
            vk = VkAds(token)
            campaign = vk.get_or_create_campaign(self.request.user, "Default Name")
            result = vk.add_ads(
                campaign_id=campaign.vk_id,
                name=ads.name,
                description=ads.description,
                image=ads.preview.file,
                link=ads.link
            )
            error = result.get('error_desc', None)
            data = {}
            if error:
                data['error'] = error
            else:
                ads.vk_url = vk.origin + 'ads?act=office&union_id={}'.format(result['id'])
                ads.save()
            return data
