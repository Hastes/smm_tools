from django.contrib import admin

from accounts.models import SmmUser


@admin.register(SmmUser)
class SmmUserAdmin(admin.ModelAdmin):
    pass