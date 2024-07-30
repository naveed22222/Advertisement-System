from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from _datetime import datetime
from django.db import connections
from django.contrib.postgres.aggregates import ArrayAgg
from django.shortcuts import render, redirect
from rest_framework.response import Response
from AppApi.serializers import *
from rest_framework.views import APIView
from django.contrib import messages



def DictinctFetchAll(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


# Create your views here.

@login_required(login_url="Login")
def DashboardView(request):
    template_name = "Dashboard.html"
    current_user = request.user
    current_date = datetime.now()
    # Delete Ads that reach Expire date
    all_ads = Ads.objects.all()
    for i in range(len(all_ads)):
        end_date = datetime.strptime(str(all_ads[i].end_date), '%Y-%m-%d')
        if end_date < current_date:
            all_ads[i].status = 'Deleted'

    cursor = connections['default'].cursor()
    query = "SELECT tbl_ads.name, start_date, end_date, lat, lng, address, status, ARRAY_AGG(tbl_location.name) AS location from tbl_ads INNER JOIN tbl_location on tbl_ads.location_id = tbl_location.id where status = 'Active' GROUP BY tbl_ads.name, start_date, end_date, lat, lng, address, status"
    cursor.execute(query)
    active_ad_list = DictinctFetchAll(cursor)

    query = "SELECT tbl_ads.name, start_date, end_date, lat, lng, address, status, ARRAY_AGG(tbl_location.name) AS location from tbl_ads INNER JOIN tbl_location on tbl_ads.location_id = tbl_location.id where status = 'Block' GROUP BY tbl_ads.name, start_date, end_date, lat, lng, address, status"
    cursor.execute(query)
    block_ad_list = DictinctFetchAll(cursor)
    context = {
        'active_ad_list': active_ad_list,
        'block_ad_list': block_ad_list,
        'current_user': current_user
    }

    return render(request, template_name, context)


@login_required(login_url="Login")
def CreateAdView(request):
    template_name = "CreateAd.html"

    if request.method == "POST":

        get_ad_name = request.POST['ad_name']
        get_start_date = request.POST['start_date']
        get_end_date = request.POST['end_date']
        get_lat = request.POST['lat']
        get_lng = request.POST['lng']
        get_location = request.POST.getlist('location')
        get_address = request.POST['address']
        if get_lat == "":
            get_lat = 0
        if get_lng == "":
            get_lng = 0

        for i in range(len(get_location)):
            create_ad = Ads(
                name=get_ad_name,
                start_date=get_start_date,
                end_date=get_end_date,
                lat=get_lat,
                lng=get_lng,
                location_id=get_location[i],
                address=get_address,
                status="Active",
            )
            create_ad.save()
        messages.success(request, "Ad Created Successfully")

    all_locations = Location.objects.all()
    context = {
        'all_locations': all_locations
    }
    return render(request, template_name, context)


@login_required(login_url="Login")
def AddLocations(request):
    template_name = "Location.html"
    DateTime = datetime.now()
    if request.method == 'POST':
        get_name = request.POST['name']
        get_visitors = request.POST['visitors']

        if get_visitors.isalpha() == True:
            messages.error(request, "Only Integer Allowed in Visitors Field")
        elif get_visitors == '':
            messages.error(request, "Visitors Field Cannot be Empty")
        else:
            duplicate_location = Location.objects.filter(name__iexact=get_name)
            if len(duplicate_location) == 0:

                Instance_location = Location(
                    name=get_name,
                    visitors=get_visitors,
                    created_at=DateTime,
                    created_by=request.user
                )
                Instance_location.save()
            else:
                messages.error(request, "The Name " + get_name + " Already Exists")

    location = Location.objects.all().order_by('name')
    context = {
        'location': location
    }
    return render(request, template_name, context)


def DeleteLocation(request, id):
    location = Location.objects.get(id=id)
    location.delete()
    return redirect('Location')


@login_required(login_url="Login")
def SingleAdView(request, id):
    template_name = "SingleAdView.html"
    # Generate Every Day Resport
    current_date = datetime.now()
    reports = DailyReports.objects.filter(date=current_date)
    if len(reports) == 0:
        all_ad_view = Ads.objects.filter(status='Active')
        for i in range(len(all_ad_view)):
            report = DailyReports(
                name=all_ad_view[i].name,
                date=current_date,
                views=1,
                location_id=all_ad_view[i].location_id
            )
            report.save()
    else:
        report_view = DailyReports.objects.filter(name=id, date=current_date)
        for i in range(len(report_view)):
            report_view[i].views += 1
            report_view[i].save()

    # Ads Views Count
    single_ad_view = Ads.objects.filter(name=id, status='Active')
    for i in range(len(single_ad_view)):
        if single_ad_view[i].status == 'Active':
            single_ad_view[i].views += 1
            single_ad_view[i].save()

        location = Location.objects.get(name=single_ad_view[i].location)
        if location.visitors <= single_ad_view[i].views:
            single_ad_view[i].status = 'Block'
            single_ad_view[i].save()
    single_ad_views = Ads.objects.filter(name=id, status='Active').values('name', 'address', 'views',
                                                                          'end_date',
                                                                          'start_date').annotate(
        location=ArrayAgg('location_id__name'))
    if len(single_ad_views) > 0:
        single_ad_views = single_ad_views[0]

    context = {
        'single_ad_view': single_ad_views,
    }

    return render(request, template_name, context)


@login_required(login_url="Login")
def DailyReportsView(request):
    template_name = "DailyAdsReport.html"
    current_date = datetime.now()
    if request.method == 'POST':
        get_date = request.POST['date']
        current_date = get_date

    daily_reports = DailyReports.objects.filter(date=current_date)
    context = {
        'daily_reports': daily_reports,
    }
    return render(request, template_name, context)


# Api Requests
class AdsDetail(APIView):

    def get(self, request):
        cb = Ads.objects.all()
        if cb.exists():
            cbSerializer = AdsSerializer(cb, many=True)
            return Response(cbSerializer.data)
        else:
            return Response("NO RECORD FOUND")


class All_location(APIView):
    def get(self, request):
        cb = Location.objects.all()
        if cb.exists():
            cbSerializer = LocationSerializers(cb, many=True)
            return Response(cbSerializer.data)
        else:
            return Response("")
