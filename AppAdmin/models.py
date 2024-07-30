from django.db import models


# Create your models here.

class Location(models.Model):
    name = models.TextField(max_length=100)
    visitors = models.IntegerField(default=100)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_location'

    def __str__(self):
        return self.name


class Ads(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.TextField(null=True, blank=True, default='Active')
    views = models.IntegerField(default=0)
    location = models.ForeignKey(Location, to_field='id', on_delete=models.CASCADE, null=True)
    lat = models.TextField(null=True, blank=True, default=0)
    lng = models.TextField(null=True, blank=True, default=0)
    address = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_ads'

    def __str__(self):
        return self.name


class DailyReports(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    views = models.IntegerField(default=0)
    location = models.ForeignKey(Location, to_field='id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'tbl_daily_reports'

    def __str__(self):
        return self.name
