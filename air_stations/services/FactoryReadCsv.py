from air_stations.services.CsvReader import CsvReader1
from ..models import FactoryReadCsvArguments

class FactoryReadCsv():
    def __init__(self, town_id = int()):
        self.town_id = town_id
        self.provider = dict({79:CsvReader1})

    def provide_csv_reader_class(self):
        frca = FactoryReadCsvArguments.objects.get(town_id = self.town_id)
        arguments = list()

        for arg in frca.arguments:
            arguments.append(arg['argument'])

        csv_reader = self.provider[self.town_id](arguments)
        return csv_reader