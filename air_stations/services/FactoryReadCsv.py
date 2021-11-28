import air_stations.services.CsvReader as CsvReader
from ..models import Arguments

class FactoryReadCsv():
    def __init__(self, town_id = int()):
        self.town_id = town_id
        self.provider = dict({79:CsvReader.CsvReader1,})

    def provide_csv_reader_class(self):
        frca = Arguments.objects.get(town_id = self.town_id, argument_type = 'ASD')
        arguments = list()

        for arg in frca.arguments:
            arguments.append(arg['argument'])

        return self.provider[self.town_id](arguments)