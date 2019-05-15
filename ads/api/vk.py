import ast
import json
import requests

from vk_api import vk_api

from ads.models import Campaign


class VkAds():

    def __init__(self, token):
        vk_session = vk_api.VkApi(token=token, api_version='5.53')
        self.vk = vk_session.get_api()
        self.origin = 'https://vk.com/'
        self.account_id = self._get_account_id()

    def _get_account_id(self):
        response = self.vk.ads.getAccounts()
        for account in response:
            if account["account_type"] == "general":
                return account['account_id']

    def add_ads(self, campaign_id, name, description, image, link):
        photo = self.upload_image(image)
        data = [{
            "campaign_id": campaign_id,
            "ad_format": 1,
            "cost_type": 1,
            "cpm": 11,
            "category1_id": 42,
            "title": name,
            "link_url" : link,
            "name": name,
            "description": description,
            "photo": photo['photo'],
            "link_domain": "mysite.com",
            "sex": 0
        }]
        result = self.vk.ads.createAds(account_id=self.account_id, data=json.dumps(data))
        return result[0]

    def upload_image(self, file):
        upload_url = self.vk.ads.getUploadURL(ad_format=1)
        return vk_upload_photo(upload_url, file)

    def get_or_create_campaign(self, user, name):
        campaign = user.campaign_set.first()
        if campaign and campaign.has_vk():
            return campaign
        data = [{
            "name": name,
            "type": 'normal',
        }]
        result = self.vk.ads.createCampaigns(account_id=self.account_id, data=json.dumps(data))
        # need to add handler
        campaign, created = Campaign.objects.get_or_create(user=user)
        campaign.vk_id = result[0]['id']
        campaign.save()
        return campaign


def vk_upload_photo(url, file):
    response = requests.post(url, files={'file': file})
    if response.status_code == 200:
        return ast.literal_eval(response.content.decode('utf-8'))
