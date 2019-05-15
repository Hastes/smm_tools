from django.contrib import admin
from ads import models


@admin.register(models.Ads)
class AdsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass
