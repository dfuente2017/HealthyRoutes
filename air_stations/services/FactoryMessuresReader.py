import HealthyRutes.air_stations.services.MessuresReader as MessuresReader

class FactoryMessuresReader():
    def __init__(self, town_id = int()):
        self.provider = dict({79:MessuresReader.MessuresReader1,})

    def provide_messures_reader(self, town = int()):
        return self.provider[town]()