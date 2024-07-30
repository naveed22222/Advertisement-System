from django.urls import re_path
from AppApi.views import *

urlpatterns = [

    re_path(r'View_all_ads/', ViewAds, name='View_all_ads'),
    re_path(r'CreateAds/', CreateAdView.as_view(), name='CreateAds'),
    re_path(r'Single_ad/(?P<id>.+)/', SingleAd, name='SingleAdView'),
    re_path(r'status/(?P<id>.+)/', AdStatusView, name='AdStatusView'),
]
