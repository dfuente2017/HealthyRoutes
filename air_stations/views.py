from urllib import response
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import AirStation, Country, Province, Town
from air_stations.services.FactoryReadCsv import FactoryReadCsv

from rest_framework.decorators import api_view
from rest_framework.response import Response as ApiResponse
from .serializers import AirStationSerializer


# Create your views here.
def upload_air_stations(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            town = int(request.POST.get('town', None))
            airStationFile = request.FILES.get('town-stations-excel', None)
            
            frc = FactoryReadCsv(town)
            csv_reader = frc.provide_csv_reader_class()
            csv_reader.read_csv(file = airStationFile, town = town)

            return redirect("/upload-air-stations")
        else:
            parameters = dict()
            parameters['countries'] = Country.objects.all()
            return render(request, "upload-air-stations.html", parameters)
    else:
        return render(request, "index.html", status=401)


#Ajax requests
def get_provinces(request):
    if request.user.is_authenticated and request.user.is_superuser:
        status = 200
        country_id = request.GET.get('country_id', -1)
        provinces = Province.objects.filter(country = country_id)
        if(len(provinces) > 0):
            response = convert_list_into_dict(provinces)
        else:
            response = dict()
            response['error'] = str('No existen provincias asociadas a ese id de pais.')
            status = 400
        return JsonResponse(response, status = status)
    else:
        return render(request, "index.html", status= 401)

def get_towns(request):
    if request.user.is_authenticated and request.user.is_superuser:
        status = 200
        province_id = request.GET.get('province_id', -1)
        towns = Town.objects.filter(province = province_id)
        if(len(towns) > 0):
            response = convert_list_into_dict(towns)
        else:
            response = dict()
            response['error'] = str('No existen ciudades asociadas a ese id de provincia.')
            status = 400
        return JsonResponse(response, status = status)
    else:
        return render(request, "index.html", status = 401)


def convert_list_into_dict(provinces = list()):
    result = dict()
    for province in provinces:
        result[province.id] = province.name
    return result


@api_view(['GET'])
def api_get_air_stations(request):
    town_id = request.GET.get('town_id', -1)
    air_stations = AirStation.objects.filter(town_id = town_id)
    if(len(air_stations) > 0):
        api_objects = AirStationSerializer(air_stations, many=True)
        return ApiResponse(api_objects.data)
    else:   
        return ApiResponse(data = None, status=400)