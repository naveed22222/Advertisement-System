from django.urls import re_path
from .views import *


urlpatterns = [
    re_path('Dashboard', DashboardView, name='Dashboard'),
    re_path('create_ads', CreateAdView, name='CreateAd'),
    re_path('Add_locations', AddLocations, name='Location'),
    re_path('delete_locations/(?P<id>.+)/', DeleteLocation, name='DeleteLocation'),
    re_path('Single_ad/(?P<id>.+)/', SingleAdView, name='SingleAd'),
    re_path('DailyReports', DailyReportsView, name='DailyReports'),


    # Api Requests
    re_path('get_all_ads', AdsDetail.as_view(), name='AdsDetailView'),
    re_path(r'All_location/', All_location.as_view(), name='All_location'),

]