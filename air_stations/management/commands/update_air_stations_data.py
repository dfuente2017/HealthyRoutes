from msilib.schema import Error
from django.core.management.base import BaseCommand, CommandError
import requests
from datetime import MINYEAR, datetime
from ...models import Town
from zope.datetime import parseDatetimetz

from ...services.FactoryMessuresReader import FactoryMessuresReader


class Command(BaseCommand):
    help = 'Updates air stations info requesting Madrid Townhall open data.'

    def add_arguments(self, parser):
        parser.add_argument('town_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            for town_id in options['town_ids']:
                town = Town.objects.get(id = town_id)
                town_saved_date = town.last_modified
                header_date = parseDatetimetz(requests.head(url = town.url).headers['Last-Modified'])

                if town_saved_date < header_date:
                    fmr = FactoryMessuresReader(town_id)
                    messures_reader = fmr.provide_messures_reader()
                    messures_reader.read_messures()
                    town.last_modified = header_date
                    town.save()
                    self.stdout.write('Se han actualizado las estaciones de calidad del aire')
                else:
                    self.stdout.write('The air stations of the town ' + str(town_id) + ' did not get saved.')
        except Error:
            raise CommandError('A problem ocurred during the command execution.')