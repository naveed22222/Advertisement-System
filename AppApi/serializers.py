from rest_framework import serializers
from AppAdmin.models import *


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ('id', 'name', 'start_date', 'end_date', 'status', 'location')

    def validate(self, data):
        status = data.get('status')
        if status != 'Active':
            raise serializers.ValidationError("Please Add Active in Status")
        return data


class LocationSerializers(serializers.ModelSerializer):
    location = AdsSerializer()

    class Meta:
        model = Location
        fields = ['id', 'name', 'visitors']


class adSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ('id', 'name', 'start_date', 'end_date', 'status', 'location')
