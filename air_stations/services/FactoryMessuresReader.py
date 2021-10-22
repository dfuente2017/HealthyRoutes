import air_stations.services.MessuresReader as MessuresReader

class FactoryMessuresReader():
    def __init__(self, town_id = int()):
        self.provider = dict({79:MessuresReader.MessuresReader1,})
        self.town_id = town_id

    def provide_messures_reader(self):
        args = list()
        return self.provider[self.town_id](args = args)