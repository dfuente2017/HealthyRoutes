import air_stations.services.MessuresReader as MessuresReader
from ..models import Arguments

class FactoryMessuresReader():
    def __init__(self, town_id = int()):
        self.provider = dict({79:MessuresReader.MessuresReader1,})
        self.town_id = town_id

    def provide_messures_reader(self):
        frca = Arguments.objects.get(town_id = self.town_id, argument_type = 'AMD')
        args = list()

        for arg in frca.arguments:
            args.append(arg['argument'])

        args.append(self.town_id)

        return self.provider[self.town_id](args = args)