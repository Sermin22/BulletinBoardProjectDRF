from django.urls import path
from ads.apps import AdsConfig
from ads.views import (AdvertisementListView, AdvertisementDetailView, AdvertisementCreateView,
                       AdvertisementUpdateView, AdvertisementDeleteView)

app_name = AdsConfig.name

urlpatterns = [
    path("ads/", AdvertisementListView.as_view(), name="ads_list"),
    path("ads/<int:pk>/", AdvertisementDetailView.as_view(), name="ads_retrieve"),
    path("ads/create/", AdvertisementCreateView.as_view(), name="ads_create"),
    path("ads/<int:pk>/update/", AdvertisementUpdateView.as_view(), name="ads_update"),
    path("ads/<int:pk>/delete/", AdvertisementDeleteView.as_view(), name="ads_delete"),
]
