from django import forms
from ads.models import Ads


class AdsCreateForm(forms.ModelForm):

    class Meta:
        model = Ads
        fields = 'name', 'description', 'preview'