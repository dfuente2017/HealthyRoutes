import requests
from datetime import MINYEAR, datetime
from ..models import Town
from zope.datetime import parseDatetimetz

from .FactoryMessuresReader import FactoryMessuresReader


def update_air_stations_data(town_id, url):
    town = Town.objects.get(id = town_id)
    town_saved_date = town.last_modified
    header_date = parseDatetimetz(requests.head(url = url).headers['Last-Modified'])

    print(town_saved_date)
    print(header_date)

    if town_saved_date < header_date:
        print("Se actualizan los datos")
        fmr = FactoryMessuresReader(town_id)
        messures_reader = fmr.provide_messures_reader()
        messures_reader.read_messures()
        town.last_modified = header_date
        town.save()
