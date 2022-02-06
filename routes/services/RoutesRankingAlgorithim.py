from air_stations.models import AirStation

class RoutesRankingAlgorithim():
    def __init__(self):
        self.air_stations = AirStation.objects.all()
        #Esto hay que cambiarlo a importar Town y sacar de ahi las estaciones de calidad del aire


    def add_air_quality_puntuation(self, routes):
        for route in routes:
            route.very_good_air_quality_nodes = 0
            route.good_air_quality_nodes = 0
            route.mediocre_air_quality_nodes = 0
            route.bad_air_quality_nodes = 0
            route.very_bad_air_quality_nodes = 0
            route.unknown_air_quality_nodes = 0

            for node in route.nodes:
                #sum_air_quality = {5:(node.very_good_air_quality_nodes += 1)}
                minimum_distance = None
                i = 0
                index = None

                for air_station in self.air_stations:
                    aux = self.distance_calculator(node['latitude'], node['longitude'], float(air_station.latitude), float(air_station.longitude))
                    if(minimum_distance == None or minimum_distance > aux):
                        minimum_distance = aux
                        index = i
                    i+= 1

                if(self.air_stations[index].air_quality == 5):
                    route.very_good_air_quality_nodes += 1
                elif(self.air_stations[index].air_quality == 4):
                    route.good_air_quality_nodes += 1
                elif(self.air_stations[index].air_quality == 3):
                    route.mediocre_air_quality_nodes += 1
                elif(self.air_stations[index].air_quality == 2):
                    route.bad_air_quality_nodes += 1
                elif(self.air_stations[index].air_quality == 1):
                    route.very_bad_air_quality_nodes += 1
                else:
                    route.unknown_air_quality_nodes +=1
            
            route.very_good_air_quality_nodes = int((route.very_good_air_quality_nodes/len(route.nodes))*100)
            route.good_air_quality_nodes = int((route.good_air_quality_nodes/len(route.nodes))*100)
            route.mediocre_air_quality_nodes = int((route.mediocre_air_quality_nodes/len(route.nodes))*100)
            route.bad_air_quality_nodes = int((route.bad_air_quality_nodes/len(route.nodes))*100)
            route.very_bad_air_quality_nodes = int((route.very_bad_air_quality_nodes/len(route.nodes))*100)
            route.unknown_air_quality_nodes = int((route.unknown_air_quality_nodes/len(route.nodes))*100)
            
        return routes
    

    def distance_calculator(self, lat1, long1, lat2, long2):
        return (((lat2-lat1)**2) + ((long2-long1)**2))**0.5


    def add_surface_quality_puntuation(self, routes):
        for route in routes:
            route.nodes_on_green_areas = None           #When the surface quality is implemented this shoul be changed to "= 0"
            route.nodes_on_non_green_areas = None       #Idem
            for node in route.nodes:
                if node['surface_quality'] != None:
                    if node['suface_quality']:
                        route.nodes_on_green_areas += 1
                    else:
                        route.nodes_on_non_green_areas += 1
        return routes


    def add_ranking_puntuation(self, routes):
        for route in routes:
            route.ranking_puntuation = 0
            
            if(not(route.very_good_air_quality_nodes == None and route.good_air_quality_nodes == None and route.mediocre_air_quality_nodes == None and route.bad_air_quality_nodes and route.very_bad_air_quality_nodes == None)):
                route.ranking_puntuation = (route.very_good_air_quality_nodes + route.good_air_quality_nodes * 0.8 + route.mediocre_air_quality_nodes * 0.5 + route.bad_air_quality_nodes * 0.2 + route.very_bad_air_quality_nodes * 0) * 0.5
            else:
                route.ranking_puntutation += 25
                
            if(not(route.nodes_on_green_areas == None and route.nodes_on_non_green_areas == None)):
                route.ranking_puntuation += route.nodes_on_green_areas*0.5
            else:
                route.ranking_puntuation += 25

            route.ranking_puntuation = round(route.ranking_puntuation, 1)
        return routes


    def sort_ranking(self, routes):
        def sort_ranking_aux(e):
            return e.ranking_puntuation

        routes.sort(reverse = True, key=sort_ranking_aux)
        return routes


