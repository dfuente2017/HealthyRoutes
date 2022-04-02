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

            return redirect("/upload-air-stations") # Enviar paises
            #return render(request, "upload-air-stations.html")
        else:
            parameters = dict()
            parameters['countries'] = Country.objects.all()
            return render(request, "upload-air-stations.html", parameters)
    else:
        #return render(request, "error page")
        return render(request, "index.html")


#Ajax requests

def get_provinces(request):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            country = request.GET.get('country_id', 0)  #Esta puesto que si no se recibe pais saque a España
            response = convert_list_into_dict(Province.objects.filter(country = country))
        except Exception as e:
            response = dict()
            response['error'] = str(e)
        return JsonResponse(response)
    else:
        #return render(request, "error page")
        return render(request, "index.html")

def get_towns(request):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            province = request.GET.get('province_id', -1)
            response = convert_list_into_dict(Town.objects.filter(province = province))
        except Exception as e:
            response = dict()
            response['error'] = str(e)
        return JsonResponse(response)
    else:
        #return render(request, "error page")
        return render(request, "index.html")


def convert_list_into_dict(provinces = list()):
    result = dict()
    for province in provinces:
        result[province.id] = province.name
    return result


@api_view(['GET'])
def api_get_air_stations(request):
    air_stations = AirStation.objects.filter(town_id = request.GET.get('town_id', 79))
    api_objects = AirStationSerializer(air_stations, many=True)
    return ApiResponse(api_objects.data)