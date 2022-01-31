from django.shortcuts import render
from numpy import RankWarning

from routes.serializers import RouteSerializer
from .services.RoutesProvider import RoutesProvider
from .services.GreenAreasProvider import GreenAreasProvider
from .services.RoutesRankingAlgorithim import RoutesRankingAlgorithim

from rest_framework.decorators import api_view
from rest_framework.response import Response as ApiResponse
from rest_framework import status

from .models import Route

from django.contrib.auth.models import auth

import json
import datetime


# Create your views here.

def index(request):
    if request.method == 'POST':
        init_lat = request.POST['initLatitude']
        init_long = request.POST['initLongitude']
        end_lat = request.POST['endLatitude']
        end_long = request.POST['endLongitude']
        variation = request.POST.get('variation', 1.5)

        rra = RoutesRankingAlgorithim()
        
        routes_provider = RoutesProvider(init_lat, init_long, end_lat, end_long, variation)
        green_areas_provider = GreenAreasProvider()
        routes = routes_provider.get_routes()
        routes = green_areas_provider.get_green_areas(routes)

        routes = rra.add_air_quality_puntuation(routes)
        routes = rra.add_surface_quality_puntuation(routes)
        routes = rra.add_ranking_puntuation(routes)
        routes = rra.sort_ranking(routes)

        return render(request, "index.html", {'routes':routes})
    else:
        return render(request, "index.html")


def saved_routes(request):
    if request.user.is_authenticated:
        return render(request, "saved-routes.html", {'routes': Route.objects.filter(user = request.user.email)})
    else:
        return render(request, "login.html")


def nodes_parser(nodes):
    nodes = list(json.loads(nodes.replace("'",'"').replace('None', 'null')))
    i = 1
    for node in nodes:
        node['id'] = i
        node['latitude'] = float(node['latitude'])
        node['longitude'] = float(node['longitude'])
        i += 1
    return nodes


def check_routes(user, distance, time, nodes, very_good_air_quality_nodes, good_air_quality_nodes, mediocre_air_quality_nodes, bad_air_quality_nodes, very_bad_air_quality_nodes, unknown_air_quality_nodes, ranking_puntuation):
    if(user == None or distance == None or time == None or nodes == None or very_good_air_quality_nodes == None or good_air_quality_nodes == None or mediocre_air_quality_nodes == None or bad_air_quality_nodes == None or very_bad_air_quality_nodes == None or unknown_air_quality_nodes == None or ranking_puntuation == None):
        raise Exception()


def api_route_post(request):
    distance = float(request.POST.get('distance',None))
    time = int(request.POST.get('time',None))
    nodes = nodes_parser(request.POST.get('nodes',None))      
    very_good_air_quality_nodes = int(request.POST.get('veryGoodAirQualityNodes',None))
    good_air_quality_nodes = int(request.POST.get('goodAirQualityNodes',None))
    mediocre_air_quality_nodes = int(request.POST.get('mediocreAirQualityNodes',None))
    bad_air_quality_nodes = int(request.POST.get('badAirQualityNodes',None))
    very_bad_air_quality_nodes= int(request.POST.get('veryBadAirQualityNodes',None))
    unknown_air_quality_nodes = int(request.POST.get('unknownAirQualityNodes',None))
    ranking_puntuation = float(request.POST.get('rankingPuntuation',None))

    check_routes(user=request.user.email, distance = distance, time = time, nodes = nodes, very_good_air_quality_nodes = very_good_air_quality_nodes, good_air_quality_nodes = good_air_quality_nodes, mediocre_air_quality_nodes = mediocre_air_quality_nodes, bad_air_quality_nodes = bad_air_quality_nodes, very_bad_air_quality_nodes = very_bad_air_quality_nodes, unknown_air_quality_nodes = unknown_air_quality_nodes, ranking_puntuation = ranking_puntuation)
    route = Route.objects.create(user=request.user.email, distance = distance, time = time, nodes = nodes, very_good_air_quality_nodes = very_good_air_quality_nodes, good_air_quality_nodes = good_air_quality_nodes, mediocre_air_quality_nodes = mediocre_air_quality_nodes, bad_air_quality_nodes = bad_air_quality_nodes, very_bad_air_quality_nodes = very_bad_air_quality_nodes, unknown_air_quality_nodes = unknown_air_quality_nodes, ranking_puntuation = ranking_puntuation)
    response = ApiResponse(data = {'message':"La ruta se ha guardado correctamente", 'route_date_saved':route.date_saved},status = status.HTTP_200_OK)

    return response


def api_route_delete(request):
    user = request.user.email
    route_date_saved = datetime.datetime.strptime(request.POST.get('routeDateSaved', None).replace('T',' ').replace('Z',''), '%Y-%m-%d %H:%M:%S.%f')

    route = Route.objects.get(user = user, date_saved = route_date_saved)
    route.delete()

    return ApiResponse(data = {'message':"La ruta ya no esta guardada"}, status = status.HTTP_200_OK)


@api_view(['POST']) # And DELETE (because of the problem that we can pass data to the ajax request)
def api_route(request):
    if request.user.is_authenticated:
        try:
            if request.POST['type'] == 'POST':
                response = api_route_post(request)
            elif request.POST['type'] == 'DELETE':
                response = api_route_delete(request)
        except Exception as e:
            print(str(e))
            response = ApiResponse(status = status.HTTP_400_BAD_REQUEST)
    else:
        response = ApiResponse(status = status.HTTP_401_UNAUTHORIZED)
    
    return response