

class GreenAreasProvider():
    def __init__(self):
        pass


    def get_green_areas(self, routes = list()):
        for route in routes:
            for node in route.nodes:
                node['surface_quality'] = None

        return routes