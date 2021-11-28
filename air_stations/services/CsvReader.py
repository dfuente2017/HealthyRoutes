import pandas as pd
from ..models import AirStation, Town

class CsvReaderInterface():
    def __init__(self, args):
        self.args = list()
        for arg in args:
            self.args.append(arg)

    def read_csv(self):
        pass


class CsvReader1(CsvReaderInterface):   #args -> [0]:ids_key, [1]: names_key, [2]: long_key, [3]: lat_key   used in: Madrid(79)
    def __init__(self, args):
        super().__init__(args)           

    def read_csv(self, file, town):
        datos = pd.read_csv(file, header = 0, sep=";")

        ids = datos[self.args[0]]
        names = datos[self.args[1]]
        longitudes = datos[self.args[2]]
        latitudes = datos[self.args[3]]

        town = Town.objects.get(id = town)

        if town.air_stations != None:
            town.air_stations = None

        town.air_stations = list()

        for i in range(len(ids)):
            air_station = {'id':ids[i], 'name': names[i], 'latitude': latitudes[i], 'longitude': longitudes[i], 'messures': None}
            town.air_stations.append(air_station)

        town.save()