import facebook

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.api import FacebookAdsApi

from ads.models import Campaign
from .facebook_user import FacebookUser


class FacebookAds():
    def __init__(self, token):
        FacebookAdsApi.init(access_token=token)
        self.account_id = FacebookUser(token).get_account_id()
        self.account = AdAccount(self.account_id)

    def add_ads(self, campaign_id, creative_id, name):
        adset = self.create_adset(campaign_id, name)
        params = {
            'name': name,
            'adset_id': adset['id'],
            'creative': {'creative_id': creative_id},
            'status': 'PAUSED',
        }
        adcreative = self.account.create_ad(params=params)
        return adcreative

    def create_adset(self, campaign_id, name):
        params = {
            AdSet.Field.name: name,
            AdSet.Field.optimization_goal: AdSet.OptimizationGoal.reach,
            AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
            AdSet.Field.bid_amount: 150,
            AdSet.Field.daily_budget: 2000,
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.targeting: {
                'geo_locations': {
                    'custom_locations': [
                        {
                            'custom_type': 'multi_city',
                            'country': 'RU',
                        },
                    ],
                    'location_types': ['recent', 'home'],
                },
            },
            AdSet.Field.status: AdSet.Status.paused,
        }
        adset = self.account.create_ad_set(
            params=params
        )
        return adset

    def create_adcreative(self, name, description, page_id, image_hash, link):
        params = {
            AdCreative.Field.name: name,
            AdCreative.Field.object_story_spec: {
                'page_id': page_id,
                'link_data': {
                    'image_hash': image_hash,
                    'link': link,
                    'message': description
                }
            }
        }
        adcreative = self.account.create_ad_creative(
            params=params
        )
        return adcreative

    def upload_image(self, file):
        image = AdImage(parent_id=self.account_id)
        image[AdImage.Field.filename] = file.path
        image.remote_create()
        return image

    def get_or_create_campaign(self, user, name):
        campaign = user.campaign_set.first()
        if campaign and campaign.has_facebook():
            return campaign
        params = {
            'name': name,
            'objective': Campaign.Objective.page_likes,
            'status': Campaign.Status.paused
        }
        adcampaign = self.account.create_campaign(
            params=params
        )
        #vulnerable
        campaign, created = Campaign.objects.get_or_create(user=user)
        campaign.facebook_id = adcampaign["id"]
        campaign.save()
        return campaign
