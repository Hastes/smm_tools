from django.urls import path
from django.views.generic import TemplateView

from accounts.views import SocialsView


urlpatterns = [
    path('', SocialsView.as_view()),
]
