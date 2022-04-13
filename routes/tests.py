from django.test import TestCase, Client
from django.conf import settings
from air_stations.models import AirStation


# Create your tests here.
class RoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = '/'
        self.saved_routes_url = '/saved-routes'
        self.api_route = '/api/route'


    #index
    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_index_POST_no_initLatitude(self):
        response = self.client.post(self.index_url,{
            'initLongitude':40,
            'endLatitude':40,
            'endLongitude':40,
            'variation':2
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response,'index.html')
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals('routes' in response.context, False)


    def test_index_POST_no_initLongitude(self):
        response = self.client.post(self.index_url,{
            'initLatitude':40,
            'endLatitude':40,
            'endLongitude':40,
            'variation':2
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response,'index.html')
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals('routes' in response.context, False)


    def test_index_POST_no_endLatitude(self):
        response = self.client.post(self.index_url,{
            'initLatitude':40,
            'initLongitude':40,
            'endLongitude':40,
            'variation':2
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response,'index.html')
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals('routes' in response.context, False)


    def test_index_POST_no_endLongitude(self):
        response = self.client.post(self.index_url,{
            'initLatitude':40,
            'initLongitude':40,
            'endLatitude':40,
            'variation':2
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response,'index.html')
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals('routes' in response.context, False)


    def test_index_POST_graphhopper_api_not_working(self):
        settings.GRAPHHOPPER_API_KEY = ''

        response = self.client.post(self.index_url,{
            'initLatitude':40,
            'initLongitude':40,
            'endLatitude':40,
            'endLongitude':40,
            'variation':2
        })

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals('routes' in response.context, False)


    def test_index_POST_correct_request(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.42047836173818, longitude = -3.7083903561337483, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.42273267370132, longitude = -3.7051278962827765, messures = None, air_quality = 1, town_id = 79)

        response = self.client.post(self.index_url,{
            'initLatitude':40.41690561266921,
            'initLongitude':-3.703417664090312,
            'endLatitude':40.42337628213949,
            'endLongitude':-3.7107446572178926,
            'variation':2
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals('error_msg' in response.context, False)
        self.assertEquals('routes' in response.context, True)

        self.assertEquals(response.context['routes'][0].ranking_puntuation > response.context['routes'][1].ranking_puntuation, True)
        self.assertEquals(response.context['routes'][1].ranking_puntuation > response.context['routes'][2].ranking_puntuation, True)

        self.assertEquals(response.context['routes'][0].very_good_air_quality_nodes, 95)
        self.assertEquals(response.context['routes'][0].very_bad_air_quality_nodes, 4)
        self.assertEquals(response.context['routes'][1].very_good_air_quality_nodes, 64)
        self.assertEquals(response.context['routes'][1].very_bad_air_quality_nodes, 35)
        self.assertEquals(response.context['routes'][2].very_good_air_quality_nodes, 31)
        self.assertEquals(response.context['routes'][2].very_bad_air_quality_nodes, 68)