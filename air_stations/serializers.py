from rest_framework import serializers
from .models import AirStation

#Rest api
class AirStationSerializer(serializers.ModelSerializer):
    class Meta():
        model = AirStation
        fields = ('id', 'name', 'latitude', 'longitude', 'messures')