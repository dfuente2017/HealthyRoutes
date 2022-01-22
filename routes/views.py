from json import dumps
from django.shortcuts import render
from .services.RoutesProvider import RoutesProvider
from .services.GreenAreasProvider import GreenAreasProvider
from .services.RoutesRankingAlgorithim import RoutesRankingAlgorithim

from rest_framework.decorators import api_view
from rest_framework.response import Response as ApiResponse


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
        print('GET')
        return render(request, "index.html")