from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.socialaccount.views import ConnectionsView
from ads.forms import AdsCreateForm
from ads.models import Ads


class SocialsView(LoginRequiredMixin, ConnectionsView):
    template_name = 'profile.html'
    success_url = reverse_lazy('get-main')

    def get_success_url(self):
        return reverse_lazy('get-main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads_create_form'] = AdsCreateForm()
        context['ads_list'] = Ads.objects.filter(user=self.request.user).order_by('-date')[:5]
        return context
