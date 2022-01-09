import requests
from .RoutesRankingAlgorithim import RoutesRankingAlgorithim
from ..models import Route


class RoutesProvider():
    def __init__(self, init_lat, init_long, end_lat, end_long, variation):
        self.init_lat = float(init_lat)
        self.init_long = float(init_long)
        self.end_lat = float(end_lat)
        self.end_long = float(end_long)
        self.variation = float(variation)


    def get_routes(self):
        rra = RoutesRankingAlgorithim()

        routes = self.routes_api_request()
        routes = self.green_areas_api_request(routes)

        routes = rra.add_air_quality_puntuation(routes)
        routes = rra.add_surface_quality_puntuation(routes)
        routes = rra.add_ranking_puntuation(routes)
        routes = rra.sort_ranking(routes)

        return routes


    def routes_api_request(self):
        routes = list()

        response = requests.get('https://graphhopper.com/api/1/route?point=' + str(self.init_lat) + ',' + str(self.init_long) + '&point=' + str(self.end_lat) + ',' + str(self.end_long) + '&vehicle=foot&locale=es&calc_points=true&key=1188f6c9-4c8b-49d2-ac9f-e9985adc8758&instructions=true&algorithm=alternative_route&points_encoded=false&ch.disable=true&alternative_route.max_paths=10&alternative_route.max_weight_factor=' + str(self.variation))
        routes_json = response.json()['paths']
        
        for route_json in routes_json:
            route = Route(distance = round(route_json['distance']/1000, 2), time = int(round(route_json['time']/60000,0))) #distancia recibida en metros y convertida a kilometros, y tiempo recibido en milisegundos y convertida a minutos
            
            nodes_json = route_json['points']['coordinates']
            nodes = list()

            for node_json in nodes_json:
                node = dict()
                node['latitude'] = node_json[0]
                node['longitude'] = node_json[1]
                node['air_quality'] = None
                node['surface_quality'] = None

                nodes.append(node)

            route.nodes = nodes

            routes.append(route)

        return routes


    def green_areas_api_request(self, routes = list()):
        pass
        return routes




        