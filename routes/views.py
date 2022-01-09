from json import dumps
from django.shortcuts import render
from .services.RoutesProvider import RoutesProvider

from rest_framework.decorators import api_view
from rest_framework.response import Response as ApiResponse


# Create your views here.

def index(request):
    if request.method == 'POST':
        print('POST')
        init_lat = request.POST['initLatitude']
        init_long = request.POST['initLongitude']
        end_lat = request.POST['endLatitude']
        end_long = request.POST['endLongitude']
        variation = request.POST.get('variation', 1.5)
        
        routes_provider = RoutesProvider(init_lat, init_long, end_lat, end_long, variation)
        routes = routes_provider.get_routes()

        #routes_json = dumps({'prueba1':'prueba1', 'prueba2':'prueba2'})
        #routes_json = dumps(routes)

        return render(request, "index.html", {'routes':routes})
    else:
        print('GET')
        return render(request, "index.html")