from django.urls import path

from ads import views


urlpatterns = [
    path('create/', views.CreateAdsView.as_view(), name='create-ads'),
    path('detail-ads/<int:pk>', views.AdsDetail.as_view(), name='get-ads'),
    path('facebook-sync/<int:ads_id>', views.CreateAdsFacebook.as_view(), name='facebook-sync'),
    path('vk-sync/<int:ads_id>', views.CreateAdsVk.as_view(), name='vk-sync'),
]
