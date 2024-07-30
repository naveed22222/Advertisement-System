from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from AppApi.serializers import *
from rest_framework import  generics
from django.http import HttpResponse


def ViewAds(request):
    template_name = "AdDetail.html"
    response = requests.get('http://localhost:7500/AppAdmin/get_all_ads')
    param = {

        'response': response.json()
    }
    return render(request, template_name, param)


class CreateAdView(generics.ListCreateAPIView):

    queryset = Ads.objects.all()
    serializer_class = AdsSerializer



@api_view(['GET', 'PUT', 'DELETE'])
def SingleAd(request, id):
    ad = Ads.objects.get(id=id)
    if ad.status == 'Active':
        ad.views += 1
        ad.save()

    if request.method == "GET":
        _serializer = adSerializer(ad)
        return Response(_serializer.data)
    elif request.method == "DELETE":
        ad.delete()
        return Response("Deleted")
    elif request.method == "PUT":
        _serializer = adSerializer(ad, data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(_serializer.data, status=200)
    return HttpResponse("Nothing Happened")


def AdStatusView(request, id):
    ad = Ads.objects.get(id=id)
    if ad.status == 'Active':
        ad.status = 'Block'
    else:
        ad.status = 'Active'
    ad.save()
    return redirect('View_all_ads')
