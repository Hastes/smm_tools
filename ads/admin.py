from django.contrib import admin
from ads import models


@admin.register(models.Ads)
class RegisterForm(admin.ModelAdmin):
    pass