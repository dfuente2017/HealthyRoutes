from routes.models import Route

from rest_framework.response import Response as ApiResponse
from rest_framework import status

import json
import datetime


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