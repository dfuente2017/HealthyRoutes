from rest_framework import serializers
from .models import Route

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['distance','time','instructions','nodes','very_good_air_quality_nodes','good_air_quality_nodes','mediocre_air_quality_nodes','bad_air_quality_nodes','very_bad_air_quality_nodes','unknown_air_quality_nodes','nodes_on_green_areas','nodes_on_non_green_areas','ranking_puntuation']