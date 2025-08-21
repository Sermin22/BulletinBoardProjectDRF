from django.urls import path
from ads.apps import AdsConfig
from ads.views import (AdvertisementListView, AdvertisementDetailView, AdvertisementCreateView,
                       AdvertisementUpdateView, AdvertisementDeleteView, CommentListView, CommentCreateView,
                       CommentDetailView, CommentUpdateView, CommentDeleteView)

app_name = AdsConfig.name

urlpatterns = [
    path("ads/", AdvertisementListView.as_view(), name="ads_list"),
    path("ads/<int:pk>/", AdvertisementDetailView.as_view(), name="ads_retrieve"),
    path("ads/create/", AdvertisementCreateView.as_view(), name="ads_create"),
    path("ads/<int:pk>/update/", AdvertisementUpdateView.as_view(), name="ads_update"),
    path("ads/<int:pk>/delete/", AdvertisementDeleteView.as_view(), name="ads_delete"),

    path("comments/", CommentListView.as_view(), name="comment_list"),
    path("comments/create/", CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment_detail"),
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),

    # вложенные: список комментариев конкретного объявления
    path("ads/<int:advertisement_id>/comments/", CommentListView.as_view(), name="ads_comments"),
    path("ads/<int:advertisement_id>/comments/create/", CommentCreateView.as_view(), name="ads_comment_create"),
]
