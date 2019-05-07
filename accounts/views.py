from django.shortcuts import render
from allauth.socialaccount.views import ConnectionsView
from ads.forms import AdsCreateForm


class SocialsView(ConnectionsView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads_create_form'] = AdsCreateForm()
        return context
