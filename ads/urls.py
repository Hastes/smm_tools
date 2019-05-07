from django.urls import path

from ads import views


urlpatterns = [
    path('create/', views.CreateAdsView.as_view(), name='create-ads'),
]
