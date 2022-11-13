from unittest import result
from xml.dom.minicompat import NodeList
from django.test import TestCase, Client
from django.conf import settings
from air_stations.models import AirStation
from routes.models import Route
from users.models import User
from routes.services.GenerateTestingDataFunctions import generate_routes_testing_data
from routes.services.EvaluationFunctions import get_results
import datetime
import json

# Create your tests here.
class RoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = '/'
        self.saved_routes_url = '/saved-routes/'
        self.api_route_url = '/api/route'
        
        User.objects.create_user(email = 'testing@testing.com', password = 'Testing12345', nick = 'testing')
        generate_routes_testing_data()


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


    #saved_routes
    def test_saved_routes_GET_no_user_logged(self):
        response = self.client.get(self.saved_routes_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)

    
    def test_saved_routes_GET_user_logged(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.get(self.saved_routes_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)

        self.assertEquals('routes' in response.context, True)
        self.assertEquals(response.context['routes'].count(), 6)

    
    def test_saved_routes_POST_no_user_logged(self):
        response = self.client.post(self.saved_routes_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_saved_routes_POST_no_operation_sent(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url)

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, True)


    def test_saved_routes_POST_incorrect_operation_sent(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url,{
            'operacion':'incorrect_operation'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, True)


    def test_saved_routes_POST_operation_order_by_no_order_by_param(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url,{
            'operation':'order-by'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, False)
        self.assertEquals('routes' in response.context, True)
        self.assertEquals(response.context['routes'].count(), 6)


    def test_saved_routes_POST_operation_order_by_incorrect_order_by_param(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url,{
            'operation':'order-by',
            'order-by':'incorrect-order-by'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals('routes' in response.context, False)
    

    def test_saved_routes_POST_operation_order_by_order_by_date_asc(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url,{
            'operation':'order-by',
            'order-by':'date-asc'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, False)
        self.assertEquals('routes' in response.context, True)
        self.assertEquals(response.context['routes'].count(), 6)
        self.assertEquals(response.context['routes'].first().time, 1)
        self.assertEquals(response.context['routes'].last().time, 6)


    def test_saved_routes_POST_operation_order_by_date_desc(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url,{
            'operation':'order-by',
            'order-by':'date-desc'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, False)
        self.assertEquals('routes' in response.context, True)
        self.assertEquals(response.context['routes'].count(), 6)
        self.assertEquals(response.context['routes'].first().time, 6)
        self.assertEquals(response.context['routes'].last().time, 1)


    def test_saved_routes_POST_operation_order_by_points(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url,{
            'operation':'order-by',
            'order-by':'points'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, False)
        self.assertEquals('routes' in response.context, True)
        self.assertEquals(len(response.context['routes']), 6)
        self.assertEquals(response.context['routes'][0].time, 2)
        self.assertEquals(response.context['routes'][5].time, 3)


    def test_saved_routes_POST_operation_order_by_distance(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.saved_routes_url,{
            'operation':'order-by',
            'order-by':'distance'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, False)
        self.assertEquals('routes' in response.context, True)
        self.assertEquals(len(response.context['routes']), 6)
        self.assertEquals(response.context['routes'][0].time, 4)
        self.assertEquals(response.context['routes'][5].time, 5)


    def test_saved_routes_POST_operation_delete_no_user_param(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        date_saved = datetime.datetime.strptime(str(Route.objects.filter(user = 'testing@testing.com').first().date_saved).replace('+', ' +'),'%Y-%m-%d %H:%M:%S.%f %z')
        date_saved = date_saved.strftime('%d-%m-%Y %H:%M:%S.%f %z')

        response = self.client.post(self.saved_routes_url,{
            'operation':'delete',
            'date-saved':date_saved
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed('saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals(Route.objects.all().count(), 7)


    def test_saved_routes_POST_operation_delete_no_date_param(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.saved_routes_url,{
            'operation':'delete',
            'user':'testing@testing.com'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed('saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals(Route.objects.all().count(), 7)


    def test_saved_routes_POST_operation_delete_incorrect_user_param(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        date_saved = datetime.datetime.strptime(str(Route.objects.filter(user = 'testing@testing.com').first().date_saved).replace('+', ' +'),'%Y-%m-%d %H:%M:%S.%f %z')
        date_saved = date_saved.strftime('%d-%m-%Y %H:%M:%S.%f %z')

        response = self.client.post(self.saved_routes_url,{
            'operation':'delete',
            'user':'othertestinguser@othertestinguser.com',
            'date-saved':date_saved
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed('saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals(Route.objects.all().count(), 7)


    def test_saved_routes_POST_operation_delete_incorrect_date_param(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        date_saved = datetime.datetime.strptime(str(Route.objects.filter(user = 'othertestinguser@othertestinguser.com').first().date_saved).replace('+', ' +'),'%Y-%m-%d %H:%M:%S.%f %z')
        date_saved = date_saved.strftime('%d-%m-%Y %H:%M:%S.%f %z')

        response = self.client.post(self.saved_routes_url,{
            'operation':'delete',
            'user':'testing@testing.com',
            'date-saved':date_saved
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed('saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, True)
        self.assertEquals(Route.objects.all().count(), 7)


    def test_saved_routes_POST_operation_delete(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        date_saved = datetime.datetime.strptime(str(Route.objects.filter(user = 'testing@testing.com').first().date_saved).replace('+', ' +'),'%Y-%m-%d %H:%M:%S.%f %z')
        date_saved1 = date_saved.strftime('%d-%m-%Y %H:%M:%S.%f %z')
        date_saved2 = date_saved.strftime('%Y-%m-%d %H:%M:%S.%f%z')

        response = self.client.post(self.saved_routes_url,{
            'operation':'delete',
            'user':'testing@testing.com',
            'date-saved': date_saved1
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('saved-routes.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals('error_msg' in response.context, False)
        self.assertEquals(Route.objects.all().count(), 6)
        self.assertEquals(list(Route.objects.filter(user = 'testing@testing.com', date_saved = date_saved2)), list())

    
    #api_route
    def test_api_route_no_user_logged(self):
        response = self.client.post(self.api_route_url)

        self.assertEquals(response.status_code, 401)
        self.assertEquals('error_msg' in json.loads(response.content), True)

        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),6)
        self.assertEquals('message' in json.loads(response.content), False)
        self.assertEquals('route_date_saved' in json.loads(response.content), False)


    def test_api_route_no_type_parameter_sent(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.api_route_url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error_msg' in json.loads(response.content), True)

        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),6)
        self.assertEquals('message' in json.loads(response.content), False)
        self.assertEquals('route_date_saved' in json.loads(response.content), False)
    

    def test_api_route_incorrect_type_parameter_sent(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.api_route_url,{
            'type':'GET'
        })

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error_msg' in json.loads(response.content), True)

        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),6)
        self.assertEquals('message' in json.loads(response.content), False)
        self.assertEquals('route_date_saved' in json.loads(response.content), False)


    def test_api_route_POST_any_parameter_not_sent(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.api_route_url,{
            'type':'POST',
            'distance':1.0,
            'time':1,
            'nodes':json.dumps([{'id':1, 'latitude':1.1, 'longitude':1.1, 'air_quality':1}, 
                                {'id':2, 'latitude':2.2, 'longitude':2.2, 'air_quality':2}]),
            'veryGoodAirQualityNodes':1,
            'goodAirQualityNodes':1,
            'mediocreAirQualityNodes':1,
            'badAirQualityNodes':1,
            'veryBadAirQualityNodes':1,
            'unknownAirQualityNodes':1,
        })

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error_msg' in json.loads(response.content), True)

        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),6)
        self.assertEquals('message' in json.loads(response.content), False)
        self.assertEquals('route_date_saved' in json.loads(response.content), False)


    def test_api_POST_correct_saved_route(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        #There are 6 routes created for this user in the setUp with the function generate_routes_testing_data()
        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),6)

        response = self.client.post(self.api_route_url,{
            'type':'POST',
            'distance':1.0,
            'time':1,
            'nodes':json.dumps([{'id':1, 'latitude':1.1, 'longitude':1.1, 'air_quality':1}, 
                                {'id':2, 'latitude':2.2, 'longitude':2.2, 'air_quality':2}]),
            'veryGoodAirQualityNodes':1,
            'goodAirQualityNodes':1,
            'mediocreAirQualityNodes':1,
            'badAirQualityNodes':1,
            'veryBadAirQualityNodes':1,
            'unknownAirQualityNodes':1,
            'rankingPuntuation':1.0,
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals('error_msg' in json.loads(response.content), False)
        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),7)
        self.assertEquals('message' in json.loads(response.content), True)
        self.assertEquals('route_date_saved' in json.loads(response.content), True)


    def test_api_DELETE_not_date_saved_sent(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.api_route_url,{
            'type':'DELETE',
        })

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error_msg' in json.loads(response.content), True)
        self.assertEquals('route_date_saved' in json.loads(response.content), False)

        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),6)
        self.assertEquals('message' in json.loads(response.content), False)


    def test_api_POST_correct_deleted_route(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        date_saved = str(datetime.datetime.strptime(str(Route.objects.filter(user = 'testing@testing.com')
                            .first().date_saved)
                            .replace('+', ' +'),'%Y-%m-%d %H:%M:%S.%f %z'))
        date_saved = date_saved[:date_saved.index("+")+1].replace(' ', 'T').replace('+','Z')             

        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),6)

        response = self.client.post(self.api_route_url,{
            'type':'DELETE',
            'routeDateSaved':date_saved
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals('error_msg' in json.loads(response.content), False)
        self.assertEquals('route_date_saved' in json.loads(response.content), False)

        self.assertEquals(len(Route.objects.filter(user = 'testing@testing.com')),5)
        self.assertEquals('message' in json.loads(response.content), True)


class Evaluation(TestCase):
    def setUp(self):
        self.threshold_failure = 0.0  #5 metros de fallo
        self.client = Client()
        self.index_url = '/'
       

    def get_obtained_route(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.3858, longitude = -3.7129, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.3858, longitude = -3.7041, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.3791, longitude = -3.7129, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 4, name = 'TestAirStation4', latitude = 40.3791, longitude = -3.7041, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.36563,
            'initLongitude': -3.61232,
            'endLatitude': 40.37565,
            'endLongitude': -3.61232,
            'variation': 20
        })

        print(response.context['routes'][0].ranking_puntuation)
        print(response.context['routes'][0].nodes)


    def evaluation1(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.46185, longitude = -3.65057, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude =  40.45709,  longitude = -3.65011, messures = None, air_quality = 1, town_id = 79)

        response = self.client.post(self.index_url,{
            'initLatitude': 40.460056,
            'initLongitude': -3.654591,
            'endLatitude': 40.458001,
            'endLongitude': -3.64393,
            'variation': 20
        })

        obtained_route = Route(nodes=  [{'longitude': -3.654591, 'latitude': 40.460056, 'air_quality': None}, 
                                        {'longitude': -3.654456, 'latitude': 40.460355, 'air_quality': None}, 
                                        {'longitude': -3.654321, 'latitude': 40.460583, 'air_quality': None}, 
                                        {'longitude': -3.654339, 'latitude': 40.460621, 'air_quality': None}, 
                                        {'longitude': -3.654332, 'latitude': 40.460667, 'air_quality': None}, 
                                        {'longitude': -3.654229, 'latitude': 40.460661, 'air_quality': None}, 
                                        {'longitude': -3.653777, 'latitude': 40.460509, 'air_quality': None}, 
                                        {'longitude': -3.653538, 'latitude': 40.460184, 'air_quality': None}, 
                                        {'longitude': -3.653334, 'latitude': 40.460029, 'air_quality': None}, 
                                        {'longitude': -3.653057, 'latitude': 40.460156, 'air_quality': None}, 
                                        {'longitude': -3.652626, 'latitude': 40.460443, 'air_quality': None}, 
                                        {'longitude': -3.652507, 'latitude': 40.460493, 'air_quality': None}, 
                                        {'longitude': -3.651282, 'latitude': 40.460732, 'air_quality': None}, 
                                        {'longitude': -3.649967, 'latitude': 40.460923, 'air_quality': None}, 
                                        {'longitude': -3.649428, 'latitude': 40.460919, 'air_quality': None}, 
                                        {'longitude': -3.649113, 'latitude': 40.460784, 'air_quality': None}, 
                                        {'longitude': -3.648805, 'latitude': 40.460588, 'air_quality': None}, 
                                        {'longitude': -3.648753, 'latitude': 40.45993, 'air_quality': None}, 
                                        {'longitude': -3.648653, 'latitude': 40.459936, 'air_quality': None}, 
                                        {'longitude': -3.648641, 'latitude': 40.459875, 'air_quality': None}, 
                                        {'longitude': -3.647974, 'latitude': 40.459947, 'air_quality': None}, 
                                        {'longitude': -3.646818, 'latitude': 40.459259, 'air_quality': None}, 
                                        {'longitude': -3.646528, 'latitude': 40.459113, 'air_quality': None}, 
                                        {'longitude': -3.646282, 'latitude': 40.459045, 'air_quality': None}, 
                                        {'longitude': -3.64648, 'latitude': 40.458595, 'air_quality': None}, 
                                        {'longitude': -3.64393, 'latitude': 40.458001, 'air_quality': None}])

        optimal_route = Route(nodes =   [{'longitude': -3.654591, 'latitude': 40.460056, 'air_quality': None}, 
                                        {'longitude': -3.654456, 'latitude': 40.460355, 'air_quality': None}, 
                                        {'longitude': -3.654321, 'latitude': 40.460583, 'air_quality': None}, 
                                        {'longitude': -3.654339, 'latitude': 40.460621, 'air_quality': None}, 
                                        {'longitude': -3.654332, 'latitude': 40.460667, 'air_quality': None}, 
                                        {'longitude': -3.654229, 'latitude': 40.460661, 'air_quality': None}, 
                                        {'longitude': -3.653777, 'latitude': 40.460509, 'air_quality': None}, 
                                        {'longitude': -3.653538, 'latitude': 40.460184, 'air_quality': None}, 
                                        {'longitude': -3.653334, 'latitude': 40.460029, 'air_quality': None}, 
                                        {'longitude': -3.653057, 'latitude': 40.460156, 'air_quality': None}, 
                                        {'longitude': -3.652626, 'latitude': 40.460443, 'air_quality': None}, 
                                        {'longitude': -3.652507, 'latitude': 40.460493, 'air_quality': None}, 
                                        {'longitude': -3.651282, 'latitude': 40.460732, 'air_quality': None}, 
                                        {'longitude': -3.649967, 'latitude': 40.460923, 'air_quality': None}, 
                                        {'longitude': -3.649428, 'latitude': 40.460919, 'air_quality': None}, 
                                        {'longitude': -3.649113, 'latitude': 40.460784, 'air_quality': None}, 
                                        {'longitude': -3.648805, 'latitude': 40.460588, 'air_quality': None}, 
                                        {'longitude': -3.648753, 'latitude': 40.45993, 'air_quality': None}, 
                                        {'longitude': -3.648653, 'latitude': 40.459936, 'air_quality': None}, 
                                        {'longitude': -3.648641, 'latitude': 40.459875, 'air_quality': None}, 
                                        {'longitude': -3.647974, 'latitude': 40.459947, 'air_quality': None}, 
                                        {'longitude': -3.64607, 'latitude': 40.46016, 'air_quality': None}, 
                                        {'longitude': -3.64589, 'latitude': 40.45932, 'air_quality': None}, 
                                        {'longitude': -3.64559, 'latitude': 40.45908, 'air_quality': None}, 
                                        {'longitude': -3.64533, 'latitude': 40.45897, 'air_quality': None}, 
                                        {'longitude': -3.64436, 'latitude': 40.45881, 'air_quality': None}, 
                                        {'longitude': -3.64408, 'latitude': 40.45886, 'air_quality': None}, 
                                        {'longitude': -3.64434, 'latitude': 40.45808, 'air_quality': None}, 
                                        {'longitude': -3.64393, 'latitude': 40.458001, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 1')


    def evaluation2(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.4597, longitude = -3.6934, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude =  40.4597,  longitude = -3.7034, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url,{
            'initLatitude': 40.4633,
            'initLongitude': -3.6983,
            'endLatitude': 40.4558,
            'endLongitude': -3.6984,
            'variation': 20
        })

        obtained_route = Route(nodes =  [{'longitude': -3.6983, 'latitude': 40.4633, 'air_quality': None},
                                        {'longitude': -3.698412, 'latitude': 40.462881, 'air_quality': None}, 
                                        {'longitude': -3.698583, 'latitude': 40.462375, 'air_quality': None}, 
                                        {'longitude': -3.698899, 'latitude': 40.462052, 'air_quality': None}, 
                                        {'longitude': -3.698853, 'latitude': 40.462036, 'air_quality': None}, 
                                        {'longitude': -3.699418, 'latitude': 40.461261, 'air_quality': None}, 
                                        {'longitude': -3.699384, 'latitude': 40.46121, 'air_quality': None}, 
                                        {'longitude': -3.699559, 'latitude': 40.461034, 'air_quality': None}, 
                                        {'longitude': -3.699472, 'latitude': 40.46102, 'air_quality': None}, 
                                        {'longitude': -3.699297, 'latitude': 40.460892, 'air_quality': None}, 
                                        {'longitude': -3.698667, 'latitude': 40.460579, 'air_quality': None}, 
                                        {'longitude': -3.698651, 'latitude': 40.460495, 'air_quality': None}, 
                                        {'longitude': -3.699209, 'latitude': 40.459924, 'air_quality': None}, 
                                        {'longitude': -3.6991, 'latitude': 40.459854, 'air_quality': None}, 
                                        {'longitude': -3.699188, 'latitude': 40.459771, 'air_quality': None}, 
                                        {'longitude': -3.698743, 'latitude': 40.459644, 'air_quality': None}, 
                                        {'longitude': -3.698934, 'latitude': 40.4592, 'air_quality': None}, 
                                        {'longitude': -3.699357, 'latitude': 40.458026, 'air_quality': None}, 
                                        {'longitude': -3.699742, 'latitude': 40.457025, 'air_quality': None}, 
                                        {'longitude': -3.700107, 'latitude': 40.456042, 'air_quality': None}, 
                                        {'longitude': -3.700317, 'latitude': 40.455308, 'air_quality': None}, 
                                        {'longitude': -3.70026, 'latitude': 40.455312, 'air_quality': None}, 
                                        {'longitude': -3.69867, 'latitude': 40.455095, 'air_quality': None},
                                        {'longitude': -3.6984, 'latitude': 40.4558, 'air_quality': None}])

        optimal_route = Route(nodes =   [{'longitude': -3.6983, 'latitude': 40.4633, 'air_quality': None}, 
                                        {'longitude': -3.698412, 'latitude': 40.462881, 'air_quality': None}, 
                                        {'longitude': -3.698583, 'latitude': 40.462375, 'air_quality': None}, 
                                        {'longitude': -3.698899, 'latitude': 40.462052, 'air_quality': None}, 
                                        {'longitude': -3.698853, 'latitude': 40.462036, 'air_quality': None}, 
                                        {'longitude': -3.699418, 'latitude': 40.461261, 'air_quality': None}, 
                                        {'longitude': -3.699384, 'latitude': 40.46121, 'air_quality': None}, 
                                        {'longitude': -3.699559, 'latitude': 40.461034, 'air_quality': None}, 
                                        {'longitude': -3.699472, 'latitude': 40.46102, 'air_quality': None}, 
                                        {'longitude': -3.699297, 'latitude': 40.460892, 'air_quality': None}, 
                                        {'longitude': -3.698667, 'latitude': 40.460579, 'air_quality': None}, 
                                        {'longitude': -3.698651, 'latitude': 40.460495, 'air_quality': None}, 
                                        {'longitude': -3.699209, 'latitude': 40.459924, 'air_quality': None}, 
                                        {'longitude': -3.6991, 'latitude': 40.459854, 'air_quality': None}, 
                                        {'longitude': -3.699188, 'latitude': 40.459771, 'air_quality': None}, 
                                        {'longitude': -3.698743, 'latitude': 40.459644, 'air_quality': None}, 
                                        {'longitude': -3.698934, 'latitude': 40.4592, 'air_quality': None},
                                        {'longitude': -3.6984, 'latitude': 40.4590, 'air_quality': None},
                                        {'longitude': -3.6987, 'latitude': 40.4579, 'air_quality': None},
                                        {'longitude': -3.6989, 'latitude': 40.4569, 'air_quality': None},
                                        {'longitude': -3.6993, 'latitude': 40.4559, 'air_quality': None},
                                        {'longitude': -3.6984, 'latitude': 40.4558, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 2')


    def evaluation3(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.41921, longitude = -3.70788, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.41082, longitude = -3.70788, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url,{
            'initLatitude': 40.415,
            'initLongitude': -3.7134,
            'endLatitude': 40.415,
            'endLongitude': -3.70246,
            'variation': 20
        })

        obtained_route = Route(nodes =  [{'longitude': -3.7134, 'latitude': 40.4150, 'air_quality': None}, 
                                        {'longitude': -3.713272, 'latitude': 40.414512, 'air_quality': None}, 
                                        {'longitude': -3.713278, 'latitude': 40.414423, 'air_quality': None}, 
                                        {'longitude': -3.713225, 'latitude': 40.414411, 'air_quality': None}, 
                                        {'longitude': -3.71273, 'latitude': 40.414476, 'air_quality': None}, 
                                        {'longitude': -3.71266, 'latitude': 40.414465, 'air_quality': None}, 
                                        {'longitude': -3.712581, 'latitude': 40.414427, 'air_quality': None}, 
                                        {'longitude': -3.712564, 'latitude': 40.414451, 'air_quality': None}, 
                                        {'longitude': -3.712419, 'latitude': 40.414527, 'air_quality': None}, 
                                        {'longitude': -3.712384, 'latitude': 40.414593, 'air_quality': None}, 
                                        {'longitude': -3.712449, 'latitude': 40.414918, 'air_quality': None}, 
                                        {'longitude': -3.71244, 'latitude': 40.414948, 'air_quality': None}, 
                                        {'longitude': -3.712409, 'latitude': 40.414966, 'air_quality': None}, 
                                        {'longitude': -3.712221, 'latitude': 40.414994, 'air_quality': None}, 
                                        {'longitude': -3.71219, 'latitude': 40.414933, 'air_quality': None}, 
                                        {'longitude': -3.711269, 'latitude': 40.414632, 'air_quality': None}, 
                                        {'longitude': -3.710386, 'latitude': 40.414288, 'air_quality': None}, 
                                        {'longitude': -3.70934, 'latitude': 40.41404, 'air_quality': None}, 
                                        {'longitude': -3.708728, 'latitude': 40.413788, 'air_quality': None}, 
                                        {'longitude': -3.708627, 'latitude': 40.413943, 'air_quality': None}, 
                                        {'longitude': -3.708566, 'latitude': 40.413888, 'air_quality': None}, 
                                        {'longitude': -3.708406, 'latitude': 40.41382, 'air_quality': None}, 
                                        {'longitude': -3.708206, 'latitude': 40.413826, 'air_quality': None}, 
                                        {'longitude': -3.708086, 'latitude': 40.413871, 'air_quality': None}, 
                                        {'longitude': -3.707567, 'latitude': 40.414108, 'air_quality': None}, 
                                        {'longitude': -3.707577, 'latitude': 40.414209, 'air_quality': None}, 
                                        {'longitude': -3.707521, 'latitude': 40.414291, 'air_quality': None}, 
                                        {'longitude': -3.707452, 'latitude': 40.414316, 'air_quality': None}, 
                                        {'longitude': -3.707269, 'latitude': 40.41433, 'air_quality': None}, 
                                        {'longitude': -3.707163, 'latitude': 40.414413, 'air_quality': None}, 
                                        {'longitude': -3.707014, 'latitude': 40.41462, 'air_quality': None}, 
                                        {'longitude': -3.706958, 'latitude': 40.414657, 'air_quality': None}, 
                                        {'longitude': -3.706011, 'latitude': 40.414803, 'air_quality': None}, 
                                        {'longitude': -3.705601, 'latitude': 40.414797, 'air_quality': None}, 
                                        {'longitude': -3.705593, 'latitude': 40.414999, 'air_quality': None}, 
                                        {'longitude': -3.704955, 'latitude': 40.414961, 'air_quality': None}, 
                                        {'longitude': -3.703967, 'latitude': 40.414729, 'air_quality': None}, 
                                        {'longitude': -3.703909, 'latitude': 40.41485, 'air_quality': None}, 
                                        {'longitude': -3.70351, 'latitude': 40.414758, 'air_quality': None}, 
                                        {'longitude': -3.703256, 'latitude': 40.414629, 'air_quality': None}, 
                                        {'longitude': -3.703045, 'latitude': 40.41457, 'air_quality': None}, 
                                        {'longitude': -3.70246, 'latitude': 40.4150, 'air_quality': None}])

        optimal_route = Route(nodes =   [{'longitude': -3.7134, 'latitude': 40.4150, 'air_quality': None}, 
                                        {'longitude': -3.713272, 'latitude': 40.414512, 'air_quality': None}, 
                                        {'longitude': -3.713278, 'latitude': 40.414423, 'air_quality': None}, 
                                        {'longitude': -3.713225, 'latitude': 40.414411, 'air_quality': None}, 
                                        {'longitude': -3.71273, 'latitude': 40.414476, 'air_quality': None}, 
                                        {'longitude': -3.71266, 'latitude': 40.414465, 'air_quality': None}, 
                                        {'longitude': -3.712581, 'latitude': 40.414427, 'air_quality': None}, 
                                        {'longitude': -3.712564, 'latitude': 40.414451, 'air_quality': None}, 
                                        {'longitude': -3.712419, 'latitude': 40.414527, 'air_quality': None}, 
                                        {'longitude': -3.712384, 'latitude': 40.414593, 'air_quality': None}, 
                                        {'longitude': -3.712449, 'latitude': 40.414918, 'air_quality': None}, 
                                        {'longitude': -3.71244, 'latitude': 40.414948, 'air_quality': None}, 
                                        {'longitude': -3.712409, 'latitude': 40.414966, 'air_quality': None}, 
                                        {'longitude': -3.712221, 'latitude': 40.414994, 'air_quality': None}, 
                                        {'longitude': -3.71219, 'latitude': 40.414933, 'air_quality': None}, 
                                        {'longitude': -3.711269, 'latitude': 40.414632, 'air_quality': None}, 
                                        {'longitude': -3.710386, 'latitude': 40.414288, 'air_quality': None}, 
                                        {'longitude': -3.70934, 'latitude': 40.41404, 'air_quality': None}, 
                                        {'longitude': -3.708728, 'latitude': 40.413788, 'air_quality': None}, 
                                        {'longitude': -3.708627, 'latitude': 40.413943, 'air_quality': None}, 
                                        {'longitude': -3.708566, 'latitude': 40.413888, 'air_quality': None}, 
                                        {'longitude': -3.708406, 'latitude': 40.41382, 'air_quality': None}, 
                                        {'longitude': -3.70765, 'latitude': 40.41357, 'air_quality': None}, 
                                        {'longitude': -3.70726, 'latitude': 40.41368, 'air_quality': None}, 
                                        {'longitude': -3.70637, 'latitude': 40.41395, 'air_quality': None}, 
                                        {'longitude': -3.70553, 'latitude': 40.41398, 'air_quality': None}, 
                                        {'longitude': -3.7048, 'latitude': 40.41395, 'air_quality': None}, 
                                        {'longitude': -3.70396, 'latitude': 40.41426, 'air_quality': None}, 
                                        {'longitude': -3.70349, 'latitude': 40.41410, 'air_quality': None}, 
                                        {'longitude': -3.703045, 'latitude': 40.41457, 'air_quality': None}, 
                                        {'longitude': -3.70246, 'latitude': 40.4150, 'air_quality': None}])
                                        
        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 3')


    def evaluation4(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.36563, longitude = -3.61232, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.37565, longitude = -3.61232, messures = None, air_quality = 1, town_id = 79)

        obtained_route = Route(nodes =  [{'longitude': -3.61232, 'latitude': 40.365632, 'air_quality': None}, 
                                        {'longitude': -3.612219, 'latitude': 40.365621, 'air_quality': None}, 
                                        {'longitude': -3.612098, 'latitude': 40.365737, 'air_quality': None}, 
                                        {'longitude': -3.611024, 'latitude': 40.367006, 'air_quality': None}, 
                                        {'longitude': -3.61202, 'latitude': 40.367491, 'air_quality': None}, 
                                        {'longitude': -3.610739, 'latitude': 40.369002, 'air_quality': None}, 
                                        {'longitude': -3.611572, 'latitude': 40.369416, 'air_quality': None}, 
                                        {'longitude': -3.611518, 'latitude': 40.369479, 'air_quality': None}, 
                                        {'longitude': -3.61168, 'latitude': 40.369559, 'air_quality': None}, 
                                        {'longitude': -3.611481, 'latitude': 40.369779, 'air_quality': None}, 
                                        {'longitude': -3.611325, 'latitude': 40.369696, 'air_quality': None}, 
                                        {'longitude': -3.611267, 'latitude': 40.36976, 'air_quality': None}, 
                                        {'longitude': -3.611424, 'latitude': 40.369837, 'air_quality': None}, 
                                        {'longitude': -3.607606, 'latitude': 40.374384, 'air_quality': None}, 
                                        {'longitude': -3.609453, 'latitude': 40.375288, 'air_quality': None}, 
                                        {'longitude': -3.609533, 'latitude': 40.37523, 'air_quality': None}, 
                                        {'longitude': -3.609636, 'latitude': 40.3752, 'air_quality': None}, 
                                        {'longitude': -3.609746, 'latitude': 40.3752, 'air_quality': None}, 
                                        {'longitude': -3.609828, 'latitude': 40.375222, 'air_quality': None}, 
                                        {'longitude': -3.609897, 'latitude': 40.375262, 'air_quality': None}, 
                                        {'longitude': -3.609948, 'latitude': 40.375316, 'air_quality': None}, 
                                        {'longitude': -3.609979, 'latitude': 40.375393, 'air_quality': None}, 
                                        {'longitude': -3.609971, 'latitude': 40.375474, 'air_quality': None}, 
                                        {'longitude': -3.609926, 'latitude': 40.375548, 'air_quality': None}, 
                                        {'longitude': -3.610766, 'latitude': 40.375933, 'air_quality': None}, 
                                        {'longitude': -3.611538, 'latitude': 40.37632, 'air_quality': None}, 
                                        {'longitude': -3.611642, 'latitude': 40.376258, 'air_quality': None}, 
                                        {'longitude': -3.611708, 'latitude': 40.376248, 'air_quality': None}, 
                                        {'longitude': -3.611807, 'latitude': 40.376265, 'air_quality': None}, 
                                        {'longitude': -3.612318, 'latitude': 40.375649, 'air_quality': None}])

        optimal_route = Route(nodes =   [{'longitude': -3.61232, 'latitude': 40.365632, 'air_quality': None}, 
                                        {'longitude': -3.612219, 'latitude': 40.365621, 'air_quality': None}, 
                                        {'longitude': -3.612098, 'latitude': 40.365737, 'air_quality': None}, 
                                        {'longitude': -3.611024, 'latitude': 40.367006, 'air_quality': None}, 
                                        {'longitude': -3.61202, 'latitude': 40.367491, 'air_quality': None}, 
                                        {'longitude': -3.610739, 'latitude': 40.369002, 'air_quality': None}, 
                                        {'longitude': -3.611572, 'latitude': 40.369416, 'air_quality': None}, 
                                        {'longitude': -3.611518, 'latitude': 40.369479, 'air_quality': None}, 
                                        {'longitude': -3.61168, 'latitude': 40.369559, 'air_quality': None}, 
                                        {'longitude': -3.611481, 'latitude': 40.369779, 'air_quality': None}, 
                                        {'longitude': -3.611325, 'latitude': 40.369696, 'air_quality': None}, 
                                        {'longitude': -3.611267, 'latitude': 40.36976, 'air_quality': None}, 
                                        {'longitude': -3.611424, 'latitude': 40.369837, 'air_quality': None}, 
                                        {'longitude': -3.607606, 'latitude': 40.374384, 'air_quality': None}, 
                                        {'longitude': -3.609453, 'latitude': 40.375288, 'air_quality': None}, 
                                        {'longitude': -3.609533, 'latitude': 40.37523, 'air_quality': None}, 
                                        {'longitude': -3.609636, 'latitude': 40.3752, 'air_quality': None}, 
                                        {'longitude': -3.609746, 'latitude': 40.3752, 'air_quality': None}, 
                                        {'longitude': -3.609828, 'latitude': 40.375222, 'air_quality': None}, 
                                        {'longitude': -3.609897, 'latitude': 40.375262, 'air_quality': None}, 
                                        {'longitude': -3.609948, 'latitude': 40.375316, 'air_quality': None}, 
                                        {'longitude': -3.609979, 'latitude': 40.375393, 'air_quality': None}, 
                                        {'longitude': -3.609971, 'latitude': 40.375474, 'air_quality': None}, 
                                        {'longitude': -3.609926, 'latitude': 40.375548, 'air_quality': None}, 
                                        {'longitude': -3.610766, 'latitude': 40.375933, 'air_quality': None}, 
                                        {'longitude': -3.611538, 'latitude': 40.37632, 'air_quality': None}, 
                                        {'longitude': -3.611642, 'latitude': 40.376258, 'air_quality': None}, 
                                        {'longitude': -3.611708, 'latitude': 40.376248, 'air_quality': None}, 
                                        {'longitude': -3.611807, 'latitude': 40.376265, 'air_quality': None}, 
                                        {'longitude': -3.612318, 'latitude': 40.375649, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 4')


    def evaluation5(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.4262, longitude = -3.6392, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.4262, longitude = -3.6322, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url,{
            'initLatitude': 40.4235,
            'initLongitude': -3.6356,
            'endLatitude': 40.42885,
            'endLongitude': -3.6356,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =  [{'longitude': -3.635598, 'latitude': 40.423568, 'air_quality': None}, 
                                        {'longitude': -3.635438, 'latitude': 40.423566, 'air_quality': None}, 
                                        {'longitude': -3.635348, 'latitude': 40.423585, 'air_quality': None}, 
                                        {'longitude': -3.635285, 'latitude': 40.423616, 'air_quality': None}, 
                                        {'longitude': -3.635045, 'latitude': 40.423774, 'air_quality': None}, 
                                        {'longitude': -3.634721, 'latitude': 40.42402, 'air_quality': None}, 
                                        {'longitude': -3.63469, 'latitude': 40.424395, 'air_quality': None}, 
                                        {'longitude': -3.634693, 'latitude': 40.424683, 'air_quality': None}, 
                                        {'longitude': -3.634675, 'latitude': 40.424773, 'air_quality': None}, 
                                        {'longitude': -3.634643, 'latitude': 40.424885, 'air_quality': None}, 
                                        {'longitude': -3.634338, 'latitude': 40.425412, 'air_quality': None}, 
                                        {'longitude': -3.634316, 'latitude': 40.42549, 'air_quality': None}, 
                                        {'longitude': -3.63441, 'latitude': 40.425621, 'air_quality': None}, 
                                        {'longitude': -3.634482, 'latitude': 40.425691, 'air_quality': None}, 
                                        {'longitude': -3.635374, 'latitude': 40.426918, 'air_quality': None}, 
                                        {'longitude': -3.635256, 'latitude': 40.427111, 'air_quality': None}, 
                                        {'longitude': -3.635265, 'latitude': 40.427169, 'air_quality': None}, 
                                        {'longitude': -3.634641, 'latitude': 40.427427, 'air_quality': None}, 
                                        {'longitude': -3.63498, 'latitude': 40.427893, 'air_quality': None}, 
                                        {'longitude': -3.634578, 'latitude': 40.428057, 'air_quality': None}, 
                                        {'longitude': -3.634676, 'latitude': 40.428193, 'air_quality': None}, 
                                        {'longitude': -3.634639, 'latitude': 40.428208, 'air_quality': None}, 
                                        {'longitude': -3.635133, 'latitude': 40.428917, 'air_quality': None}, 
                                        {'longitude': -3.635377, 'latitude': 40.428856, 'air_quality': None}, 
                                        {'longitude': -3.6356, 'latitude': 40.428837, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 5')

    
    def evaluation6(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.44925, longitude = -3.7144, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.43737, longitude = -3.70874, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.43737, longitude = -3.7201, messures = None, air_quality = 1, town_id = 79)

        obtained_route = Route(nodes =  [{'longitude': -3.722796, 'latitude': 40.4439, 'air_quality': None}, 
                                        {'longitude': -3.722796, 'latitude': 40.443903, 'air_quality': None}, 
                                        {'longitude': -3.721784, 'latitude': 40.444037, 'air_quality': None}, 
                                        {'longitude': -3.721449, 'latitude': 40.443994, 'air_quality': None}, 
                                        {'longitude': -3.72086, 'latitude': 40.444024, 'air_quality': None}, 
                                        {'longitude': -3.720763, 'latitude': 40.443431, 'air_quality': None}, 
                                        {'longitude': -3.719835, 'latitude': 40.443453, 'air_quality': None}, 
                                        {'longitude': -3.719686, 'latitude': 40.443439, 'air_quality': None}, 
                                        {'longitude': -3.719475, 'latitude': 40.443375, 'air_quality': None}, 
                                        {'longitude': -3.71949, 'latitude': 40.443538, 'air_quality': None}, 
                                        {'longitude': -3.719468, 'latitude': 40.443611, 'air_quality': None}, 
                                        {'longitude': -3.719389, 'latitude': 40.443684, 'air_quality': None}, 
                                        {'longitude': -3.717264, 'latitude': 40.443502, 'air_quality': None}, 
                                        {'longitude': -3.716737, 'latitude': 40.443471, 'air_quality': None}, 
                                        {'longitude': -3.716075, 'latitude': 40.443488, 'air_quality': None}, 
                                        {'longitude': -3.715627, 'latitude': 40.443598, 'air_quality': None}, 
                                        {'longitude': -3.715408, 'latitude': 40.443708, 'air_quality': None}, 
                                        {'longitude': -3.715209, 'latitude': 40.443839, 'air_quality': None}, 
                                        {'longitude': -3.715121, 'latitude': 40.443929, 'air_quality': None}, 
                                        {'longitude': -3.714888, 'latitude': 40.444285, 'air_quality': None}, 
                                        {'longitude': -3.71484, 'latitude': 40.444565, 'air_quality': None}, 
                                        {'longitude': -3.714827, 'latitude': 40.444883, 'air_quality': None}, 
                                        {'longitude': -3.712375, 'latitude': 40.444775, 'air_quality': None}, 
                                        {'longitude': -3.710552, 'latitude': 40.444682, 'air_quality': None}, 
                                        {'longitude': -3.710328, 'latitude': 40.444514, 'air_quality': None}, 
                                        {'longitude': -3.710115, 'latitude': 40.444426, 'air_quality': None}, 
                                        {'longitude': -3.710028, 'latitude': 40.444433, 'air_quality': None}, 
                                        {'longitude': -3.707936, 'latitude': 40.445727, 'air_quality': None}, 
                                        {'longitude': -3.707802, 'latitude': 40.445605, 'air_quality': None}, 
                                        {'longitude': -3.707562, 'latitude': 40.445749, 'air_quality': None}, 
                                        {'longitude': -3.707302, 'latitude': 40.44557, 'air_quality': None}, 
                                        {'longitude': -3.706893, 'latitude': 40.445185, 'air_quality': None}, 
                                        {'longitude': -3.706496, 'latitude': 40.444559, 'air_quality': None}, 
                                        {'longitude': -3.706419, 'latitude': 40.444585, 'air_quality': None}, 
                                        {'longitude': -3.706294, 'latitude': 40.444311, 'air_quality': None}, 
                                        {'longitude': -3.706031, 'latitude': 40.443889, 'air_quality': None}])

        optimal_route = Route(nodes =   [{'longitude': -3.722796, 'latitude': 40.4439, 'air_quality': None}, 
                                        {'longitude': -3.722796, 'latitude': 40.443903, 'air_quality': None}, 
                                        {'longitude': -3.721784, 'latitude': 40.444037, 'air_quality': None}, 
                                        {'longitude': -3.721449, 'latitude': 40.443994, 'air_quality': None}, 
                                        {'longitude': -3.72086, 'latitude': 40.444024, 'air_quality': None}, 
                                        {'longitude': -3.72108, 'latitude': 40.44539, 'air_quality': None},
                                        {'longitude': -3.72095, 'latitude': 40.44553, 'air_quality': None},
                                        {'longitude': -3.72030, 'latitude': 40.44569, 'air_quality': None},
                                        {'longitude': -3.72003, 'latitude': 40.44599, 'air_quality': None},
                                        {'longitude': -3.71959, 'latitude': 40.44659, 'air_quality': None},
                                        {'longitude': -3.71904, 'latitude': 40.44680, 'air_quality': None},
                                        {'longitude': -3.71814, 'latitude': 40.44671, 'air_quality': None},
                                        {'longitude': -3.71733, 'latitude': 40.44668, 'air_quality': None},
                                        {'longitude': -3.71473, 'latitude': 40.44578, 'air_quality': None},
                                        {'longitude': -3.714827, 'latitude': 40.444883, 'air_quality': None}, 
                                        {'longitude': -3.712375, 'latitude': 40.444775, 'air_quality': None}, 
                                        {'longitude': -3.710552, 'latitude': 40.444682, 'air_quality': None}, 
                                        {'longitude': -3.710328, 'latitude': 40.444514, 'air_quality': None}, 
                                        {'longitude': -3.710115, 'latitude': 40.444426, 'air_quality': None}, 
                                        {'longitude': -3.710028, 'latitude': 40.444433, 'air_quality': None}, 
                                        {'longitude': -3.707936, 'latitude': 40.445727, 'air_quality': None}, 
                                        {'longitude': -3.707802, 'latitude': 40.445605, 'air_quality': None}, 
                                        {'longitude': -3.707562, 'latitude': 40.445749, 'air_quality': None}, 
                                        {'longitude': -3.707302, 'latitude': 40.44557, 'air_quality': None}, 
                                        {'longitude': -3.706893, 'latitude': 40.445185, 'air_quality': None}, 
                                        {'longitude': -3.706496, 'latitude': 40.444559, 'air_quality': None}, 
                                        {'longitude': -3.706419, 'latitude': 40.444585, 'air_quality': None}, 
                                        {'longitude': -3.706294, 'latitude': 40.444311, 'air_quality': None}, 
                                        {'longitude': -3.706031, 'latitude': 40.443889, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 6')
    

    def evaluation7(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.37632, longitude = -3.72756, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.39125, longitude = -3.721, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.39125, longitude = -3.7145, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url,{
            'initLatitude': 40.38387,
            'initLongitude': -3.73073,
            'endLatitude': 40.38387,
            'endLongitude': -3.7113,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =  [{'longitude': -3.730724, 'latitude': 40.38386, 'air_quality': None}, 
                                        {'longitude': -3.730549, 'latitude': 40.383922, 'air_quality': None}, 
                                        {'longitude': -3.730417, 'latitude': 40.383879, 'air_quality': None}, 
                                        {'longitude': -3.729291, 'latitude': 40.383611, 'air_quality': None}, 
                                        {'longitude': -3.726506, 'latitude': 40.383632, 'air_quality': None}, 
                                        {'longitude': -3.725575, 'latitude': 40.383576, 'air_quality': None}, 
                                        {'longitude': -3.725132, 'latitude': 40.383533, 'air_quality': None}, 
                                        {'longitude': -3.724924, 'latitude': 40.383411, 'air_quality': None}, 
                                        {'longitude': -3.724491, 'latitude': 40.382904, 'air_quality': None}, 
                                        {'longitude': -3.724009, 'latitude': 40.382434, 'air_quality': None}, 
                                        {'longitude': -3.72367, 'latitude': 40.382712, 'air_quality': None}, 
                                        {'longitude': -3.723371, 'latitude': 40.382854, 'air_quality': None}, 
                                        {'longitude': -3.722931, 'latitude': 40.382411, 'air_quality': None}, 
                                        {'longitude': -3.722927, 'latitude': 40.382371, 'air_quality': None}, 
                                        {'longitude': -3.722585, 'latitude': 40.381996, 'air_quality': None}, 
                                        {'longitude': -3.722225, 'latitude': 40.381602, 'air_quality': None}, 
                                        {'longitude': -3.721692, 'latitude': 40.381073, 'air_quality': None}, 
                                        {'longitude': -3.721423, 'latitude': 40.380859, 'air_quality': None}, 
                                        {'longitude': -3.720786, 'latitude': 40.380632, 'air_quality': None}, 
                                        {'longitude': -3.720277, 'latitude': 40.380558, 'air_quality': None}, 
                                        {'longitude': -3.71982, 'latitude': 40.380547, 'air_quality': None}, 
                                        {'longitude': -3.71935, 'latitude': 40.38049, 'air_quality': None}, 
                                        {'longitude': -3.719117, 'latitude': 40.380422, 'air_quality': None}, 
                                        {'longitude': -3.719146, 'latitude': 40.380089, 'air_quality': None}, 
                                        {'longitude': -3.71912, 'latitude': 40.380087, 'air_quality': None}, 
                                        {'longitude': -3.719087, 'latitude': 40.380287, 'air_quality': None}, 
                                        {'longitude': -3.718749, 'latitude': 40.380254, 'air_quality': None}, 
                                        {'longitude': -3.718762, 'latitude': 40.380069, 'air_quality': None}, 
                                        {'longitude': -3.71873, 'latitude': 40.380086, 'air_quality': None}, 
                                        {'longitude': -3.718696, 'latitude': 40.380394, 'air_quality': None}, 
                                        {'longitude': -3.717826, 'latitude': 40.380393, 'air_quality': None}, 
                                        {'longitude': -3.717678, 'latitude': 40.381386, 'air_quality': None}, 
                                        {'longitude': -3.716087, 'latitude': 40.381359, 'air_quality': None}, 
                                        {'longitude': -3.715651, 'latitude': 40.381836, 'air_quality': None}, 
                                        {'longitude': -3.715154, 'latitude': 40.382554, 'air_quality': None}, 
                                        {'longitude': -3.715141, 'latitude': 40.382631, 'air_quality': None}, 
                                        {'longitude': -3.713886, 'latitude': 40.382646, 'air_quality': None}, 
                                        {'longitude': -3.713392, 'latitude': 40.382669, 'air_quality': None}, 
                                        {'longitude': -3.713132, 'latitude': 40.382663, 'air_quality': None}, 
                                        {'longitude': -3.711253, 'latitude': 40.382699, 'air_quality': None}, 
                                        {'longitude': -3.711266, 'latitude': 40.383725, 'air_quality': None}, 
                                        {'longitude': -3.711295, 'latitude': 40.383871, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 7')


    def evaluation8(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.4935, longitude = -3.71933, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.49027, longitude = -3.71933, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.4872, longitude = -3.73186, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.495,
            'initLongitude': -3.7256,
            'endLatitude': 40.4855,
            'endLongitude': -3.7256,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.725594, 'latitude': 40.494996, 'air_quality': None}, 
                                        {'longitude': -3.726555, 'latitude': 40.494151, 'air_quality': None}, 
                                        {'longitude': -3.726617, 'latitude': 40.494067, 'air_quality': None}, 
                                        {'longitude': -3.726697, 'latitude': 40.494096, 'air_quality': None}, 
                                        {'longitude': -3.726785, 'latitude': 40.494095, 'air_quality': None}, 
                                        {'longitude': -3.726863, 'latitude': 40.494064, 'air_quality': None}, 
                                        {'longitude': -3.726914, 'latitude': 40.49401, 'air_quality': None}, 
                                        {'longitude': -3.726929, 'latitude': 40.493943, 'air_quality': None}, 
                                        {'longitude': -3.726902, 'latitude': 40.493879, 'air_quality': None}, 
                                        {'longitude': -3.727638, 'latitude': 40.493208, 'air_quality': None}, 
                                        {'longitude': -3.727949, 'latitude': 40.492967, 'air_quality': None}, 
                                        {'longitude': -3.728338, 'latitude': 40.4927, 'air_quality': None}, 
                                        {'longitude': -3.729473, 'latitude': 40.492096, 'air_quality': None}, 
                                        {'longitude': -3.730108, 'latitude': 40.4917, 'air_quality': None}, 
                                        {'longitude': -3.730528, 'latitude': 40.491404, 'air_quality': None}, 
                                        {'longitude': -3.732752, 'latitude': 40.489602, 'air_quality': None}, 
                                        {'longitude': -3.732865, 'latitude': 40.489542, 'air_quality': None}, 
                                        {'longitude': -3.732776, 'latitude': 40.489499, 'air_quality': None}, 
                                        {'longitude': -3.732746, 'latitude': 40.489465, 'air_quality': None}, 
                                        {'longitude': -3.732729, 'latitude': 40.489253, 'air_quality': None}, 
                                        {'longitude': -3.732703, 'latitude': 40.489204, 'air_quality': None}, 
                                        {'longitude': -3.731734, 'latitude': 40.488011, 'air_quality': None}, 
                                        {'longitude': -3.731653, 'latitude': 40.487949, 'air_quality': None}, 
                                        {'longitude': -3.731525, 'latitude': 40.487932, 'air_quality': None}, 
                                        {'longitude': -3.731474, 'latitude': 40.4879, 'air_quality': None}, 
                                        {'longitude': -3.731426, 'latitude': 40.48781, 'air_quality': None}, 
                                        {'longitude': -3.731462, 'latitude': 40.487716, 'air_quality': None}, 
                                        {'longitude': -3.730929, 'latitude': 40.487019, 'air_quality': None}, 
                                        {'longitude': -3.73077, 'latitude': 40.486889, 'air_quality': None}, 
                                        {'longitude': -3.730573, 'latitude': 40.486826, 'air_quality': None}, 
                                        {'longitude': -3.730496, 'latitude': 40.486811, 'air_quality': None}, 
                                        {'longitude': -3.730397, 'latitude': 40.486765, 'air_quality': None}, 
                                        {'longitude': -3.730339, 'latitude': 40.486716, 'air_quality': None}, 
                                        {'longitude': -3.730292, 'latitude': 40.486635, 'air_quality': None}, 
                                        {'longitude': -3.730283, 'latitude': 40.486555, 'air_quality': None}, 
                                        {'longitude': -3.730332, 'latitude': 40.486441, 'air_quality': None}, 
                                        {'longitude': -3.729997, 'latitude': 40.486376, 'air_quality': None}, 
                                        {'longitude': -3.728285, 'latitude': 40.485721, 'air_quality': None}, 
                                        {'longitude': -3.727977, 'latitude': 40.48561, 'air_quality': None}, 
                                        {'longitude': -3.727621, 'latitude': 40.485544, 'air_quality': None}, 
                                        {'longitude': -3.7256, 'latitude': 40.485532, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 8')


    def evaluation9(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.48005, longitude = -3.65357, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.47674, longitude = -3.66653, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.4734, longitude = -3.66653, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.48133,
            'initLongitude': -3.65899,
            'endLatitude': 40.4714,
            'endLongitude': -3.65899,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.658979, 'latitude': 40.481328, 'air_quality': None}, 
                                        {'longitude': -3.658975, 'latitude': 40.481339, 'air_quality': None}, 
                                        {'longitude': -3.656899, 'latitude': 40.480694, 'air_quality': None}, 
                                        {'longitude': -3.655872, 'latitude': 40.480418, 'air_quality': None}, 
                                        {'longitude': -3.655765, 'latitude': 40.480359, 'air_quality': None}, 
                                        {'longitude': -3.655729, 'latitude': 40.480289, 'air_quality': None}, 
                                        {'longitude': -3.65574, 'latitude': 40.480187, 'air_quality': None}, 
                                        {'longitude': -3.656547, 'latitude': 40.477873, 'air_quality': None}, 
                                        {'longitude': -3.656592, 'latitude': 40.477362, 'air_quality': None}, 
                                        {'longitude': -3.656659, 'latitude': 40.475266, 'air_quality': None}, 
                                        {'longitude': -3.656352, 'latitude': 40.47526, 'air_quality': None}, 
                                        {'longitude': -3.655836, 'latitude': 40.475177, 'air_quality': None}, 
                                        {'longitude': -3.65705, 'latitude': 40.47432, 'air_quality': None}, 
                                        {'longitude': -3.65741, 'latitude': 40.47406, 'air_quality': None}, 
                                        {'longitude': -3.65876, 'latitude': 40.47309, 'air_quality': None}, 
                                        {'longitude': -3.65948, 'latitude': 40.47259, 'air_quality': None}, 
                                        {'longitude': -3.66042, 'latitude': 40.47191, 'air_quality': None}, 
                                        {'longitude': -3.659017, 'latitude': 40.471359, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 9')


    def evaluation10(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.36044, longitude = -3.76142, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.38127, longitude = -3.75239, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.38127, longitude = -3.7434, messures = None, air_quality = 1, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.37086,
            'initLongitude': -3.76597,
            'endLatitude': 40.37086,
            'endLongitude': -3.7388,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.765967, 'latitude': 40.37086, 'air_quality': None}, 
                                        {'longitude': -3.765965, 'latitude': 40.370873, 'air_quality': None}, 
                                        {'longitude': -3.764766, 'latitude': 40.370748, 'air_quality': None}, 
                                        {'longitude': -3.764784, 'latitude': 40.370617, 'air_quality': None}, 
                                        {'longitude': -3.762695, 'latitude': 40.370391, 'air_quality': None}, 
                                        {'longitude': -3.762785, 'latitude': 40.369914, 'air_quality': None}, 
                                        {'longitude': -3.762714, 'latitude': 40.369873, 'air_quality': None}, 
                                        {'longitude': -3.762479, 'latitude': 40.369845, 'air_quality': None}, 
                                        {'longitude': -3.760962, 'latitude': 40.369693, 'air_quality': None}, 
                                        {'longitude': -3.76018, 'latitude': 40.369242, 'air_quality': None}, 
                                        {'longitude': -3.759818, 'latitude': 40.36913, 'air_quality': None}, 
                                        {'longitude': -3.757671, 'latitude': 40.368334, 'air_quality': None}, 
                                        {'longitude': -3.755535, 'latitude': 40.369321, 'air_quality': None}, 
                                        {'longitude': -3.754636, 'latitude': 40.369787, 'air_quality': None}, 
                                        {'longitude': -3.753758, 'latitude': 40.370056, 'air_quality': None}, 
                                        {'longitude': -3.752557, 'latitude': 40.370377, 'air_quality': None}, 
                                        {'longitude': -3.752164, 'latitude': 40.370526, 'air_quality': None}, 
                                        {'longitude': -3.751629, 'latitude': 40.370824, 'air_quality': None}, 
                                        {'longitude': -3.751538, 'latitude': 40.370512, 'air_quality': None}, 
                                        {'longitude': -3.751468, 'latitude': 40.370473, 'air_quality': None}, 
                                        {'longitude': -3.75032, 'latitude': 40.370737, 'air_quality': None}, 
                                        {'longitude': -3.74926, 'latitude': 40.370932, 'air_quality': None}, 
                                        {'longitude': -3.749058, 'latitude': 40.3707, 'air_quality': None}, 
                                        {'longitude': -3.747118, 'latitude': 40.371273, 'air_quality': None}, 
                                        {'longitude': -3.746384, 'latitude': 40.37162, 'air_quality': None}, 
                                        {'longitude': -3.745956, 'latitude': 40.3717, 'air_quality': None}, 
                                        {'longitude': -3.74436, 'latitude': 40.371676, 'air_quality': None}, 
                                        {'longitude': -3.743021, 'latitude': 40.371601, 'air_quality': None}, 
                                        {'longitude': -3.742379, 'latitude': 40.371556, 'air_quality': None}, 
                                        {'longitude': -3.739949, 'latitude': 40.369842, 'air_quality': None}, 
                                        {'longitude': -3.739169, 'latitude': 40.370455, 'air_quality': None}, 
                                        {'longitude': -3.73882, 'latitude': 40.370867, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 10')


    def evaluation11(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.4777, longitude = -3.5917, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.4777, longitude = -3.5805, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.4695, longitude = -3.5917, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 4, name = 'TestAirStation4', latitude = 40.4695, longitude = -3.5805, messures = None, air_quality = 1, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.47358,
            'initLongitude': -3.59665,
            'endLatitude': 40.47358,
            'endLongitude': -3.57526,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.596645, 'latitude': 40.473581, 'air_quality': None}, 
                                        {'longitude': -3.596648, 'latitude': 40.473593, 'air_quality': None}, 
                                        {'longitude': -3.596393, 'latitude': 40.473723, 'air_quality': None}, 
                                        {'longitude': -3.59602, 'latitude': 40.473888, 'air_quality': None}, 
                                        {'longitude': -3.595794, 'latitude': 40.473954, 'air_quality': None}, 
                                        {'longitude': -3.595485, 'latitude': 40.474001, 'air_quality': None}, 
                                        {'longitude': -3.59522, 'latitude': 40.474011, 'air_quality': None}, 
                                        {'longitude': -3.594654, 'latitude': 40.473936, 'air_quality': None}, 
                                        {'longitude': -3.59439, 'latitude': 40.47387, 'air_quality': None}, 
                                        {'longitude': -3.5934, 'latitude': 40.474459, 'air_quality': None}, 
                                        {'longitude': -3.593244, 'latitude': 40.474503, 'air_quality': None}, 
                                        {'longitude': -3.593239, 'latitude': 40.474911, 'air_quality': None}, 
                                        {'longitude': -3.589791, 'latitude': 40.474893, 'air_quality': None}, 
                                        {'longitude': -3.586147, 'latitude': 40.474855, 'air_quality': None}, 
                                        {'longitude': -3.586103, 'latitude': 40.474829, 'air_quality': None}, 
                                        {'longitude': -3.58528, 'latitude': 40.47554, 'air_quality': None}, 
                                        {'longitude': -3.585168, 'latitude': 40.475485, 'air_quality': None}, 
                                        {'longitude': -3.585083, 'latitude': 40.475475, 'air_quality': None}, 
                                        {'longitude': -3.584934, 'latitude': 40.475494, 'air_quality': None}, 
                                        {'longitude': -3.584854, 'latitude': 40.475554, 'air_quality': None}, 
                                        {'longitude': -3.584818, 'latitude': 40.475606, 'air_quality': None}, 
                                        {'longitude': -3.584795, 'latitude': 40.475729, 'air_quality': None}, 
                                        {'longitude': -3.583268, 'latitude': 40.475712, 'air_quality': None}, 
                                        {'longitude': -3.582753, 'latitude': 40.475646, 'air_quality': None}, 
                                        {'longitude': -3.582578, 'latitude': 40.475641, 'air_quality': None}, 
                                        {'longitude': -3.582442, 'latitude': 40.475549, 'air_quality': None}, 
                                        {'longitude': -3.582317, 'latitude': 40.475474, 'air_quality': None}, 
                                        {'longitude': -3.582192, 'latitude': 40.475426, 'air_quality': None}, 
                                        {'longitude': -3.582003, 'latitude': 40.475521, 'air_quality': None}, 
                                        {'longitude': -3.5816, 'latitude': 40.475203, 'air_quality': None}, 
                                        {'longitude': -3.58127, 'latitude': 40.474899, 'air_quality': None}, 
                                        {'longitude': -3.581229, 'latitude': 40.474962, 'air_quality': None}, 
                                        {'longitude': -3.581066, 'latitude': 40.475091, 'air_quality': None}, 
                                        {'longitude': -3.580408, 'latitude': 40.475413, 'air_quality': None}, 
                                        {'longitude': -3.580305, 'latitude': 40.475424, 'air_quality': None}, 
                                        {'longitude': -3.579422, 'latitude': 40.475785, 'air_quality': None}, 
                                        {'longitude': -3.579409, 'latitude': 40.475743, 'air_quality': None},
                                        {'longitude': -3.57827, 'latitude': 40.47610, 'air_quality': None},
                                        {'longitude': -3.57723, 'latitude': 40.47561, 'air_quality': None},
                                        {'longitude': -3.57646, 'latitude': 40.4749, 'air_quality': None},
                                        {'longitude': -3.57658, 'latitude': 40.47482, 'air_quality': None},
                                        {'longitude': -3.57629, 'latitude': 40.47453, 'air_quality': None},
                                        {'longitude': -3.575661, 'latitude': 40.473421, 'air_quality': None}, 
                                        {'longitude': -3.575, 'latitude': 40.47406, 'air_quality': None}, 
                                        {'longitude': -3.57491, 'latitude': 40.47385, 'air_quality': None}, 
                                        {'longitude': -3.575259, 'latitude': 40.473579, 'air_quality': None}])
        
        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 11')


    def evaluation12(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.44198, longitude = -3.65183, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.4377, longitude = -3.65183, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.44198, longitude = -3.65739, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 4, name = 'TestAirStation4', latitude = 40.4377, longitude = -3.65739, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.44413,
            'initLongitude': -3.65465,
            'endLatitude': 40.4356,
            'endLongitude': -3.65465,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.654642, 'latitude': 40.444133, 'air_quality': None}, 
                                        {'longitude': -3.654646, 'latitude': 40.444139, 'air_quality': None}, 
                                        {'longitude': -3.655536, 'latitude': 40.443976, 'air_quality': None}, 
                                        {'longitude': -3.65475, 'latitude': 40.44178, 'air_quality': None},
                                        {'longitude': -3.65546, 'latitude': 40.44131, 'air_quality': None},
                                        {'longitude': -3.6551, 'latitude': 40.44018, 'air_quality': None},
                                        {'longitude': -3.65477, 'latitude': 40.43917, 'air_quality': None},
                                        {'longitude': -3.65564, 'latitude': 40.439, 'air_quality': None},
                                        {'longitude': -3.65542, 'latitude': 40.43832, 'air_quality': None},
                                        {'longitude': -3.65509, 'latitude': 40.43733, 'air_quality': None},
                                        {'longitude': -3.6553, 'latitude': 40.43695, 'air_quality': None},
                                        {'longitude': -3.65508, 'latitude': 40.43678, 'air_quality': None},
                                        {'longitude': -3.655526, 'latitude': 40.435306, 'air_quality': None}, 
                                        {'longitude': -3.654751, 'latitude': 40.435656, 'air_quality': None}, 
                                        {'longitude': -3.654664, 'latitude': 40.435655, 'air_quality': None}, 
                                        {'longitude': -3.654679, 'latitude': 40.435616, 'air_quality': None}, 
                                        {'longitude': -3.654648, 'latitude': 40.435603, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 12')


    def evaluation13(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.42673, longitude = -3.6816, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.42032, longitude = 3.6816, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.42673, longitude = -3.67316, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 4, name = 'TestAirStation4', latitude = 40.42032, longitude = -3.67316, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.42995, 
            'initLongitude': -3.67721,
            'endLatitude': 40.41709,
            'endLongitude': -3.67738,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.677207, 'latitude': 40.429981, 'air_quality': None}, 
                                        {'longitude': -3.676815, 'latitude': 40.429962, 'air_quality': None}, 
                                        {'longitude': -3.677238, 'latitude': 40.424862, 'air_quality': None}, 
                                        {'longitude': -3.677278, 'latitude': 40.424076, 'air_quality': None}, 
                                        {'longitude': -3.677527, 'latitude': 40.421581, 'air_quality': None}, 
                                        {'longitude': -3.677837, 'latitude': 40.418214, 'air_quality': None}, 
                                        {'longitude': -3.677777, 'latitude': 40.418211, 'air_quality': None}, 
                                        {'longitude': -3.677862, 'latitude': 40.417192, 'air_quality': None}, 
                                        {'longitude': -3.677836, 'latitude': 40.417165, 'air_quality': None}, 
                                        {'longitude': -3.67784, 'latitude': 40.417116, 'air_quality': None}, 
                                        {'longitude': -3.67738, 'latitude': 40.417092, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 13')


    def evaluation14(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.35782, longitude = -3.6936, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.35054, longitude = -3.6936, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.35782, longitude = -3.68416, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 4, name = 'TestAirStation4', latitude = 40.35054, longitude = -3.68416, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.36144, 
            'initLongitude': -3.68886,
            'endLatitude': 40.34684,
            'endLongitude': -3.68886,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.68886, 'latitude': 40.361441, 'air_quality': None}, 
                                        {'longitude': -3.689258, 'latitude': 40.361426, 'air_quality': None}, 
                                        {'longitude': -3.689558, 'latitude': 40.361343, 'air_quality': None}, 
                                        {'longitude': -3.689686, 'latitude': 40.361175, 'air_quality': None}, 
                                        {'longitude': -3.68966, 'latitude': 40.360631, 'air_quality': None}, 
                                        {'longitude': -3.689659, 'latitude': 40.360015, 'air_quality': None}, 
                                        {'longitude': -3.689626, 'latitude': 40.359438, 'air_quality': None}, 
                                        {'longitude': -3.689604, 'latitude': 40.359343, 'air_quality': None}, 
                                        {'longitude': -3.689536, 'latitude': 40.359331, 'air_quality': None}, 
                                        {'longitude': -3.689432, 'latitude': 40.359284, 'air_quality': None}, 
                                        {'longitude': -3.689366, 'latitude': 40.359217, 'air_quality': None}, 
                                        {'longitude': -3.689339, 'latitude': 40.359102, 'air_quality': None}, 
                                        {'longitude': -3.689375, 'latitude': 40.358992, 'air_quality': None}, 
                                        {'longitude': -3.689496, 'latitude': 40.358886, 'air_quality': None}, 
                                        {'longitude': -3.68954, 'latitude': 40.358873, 'air_quality': None}, 
                                        {'longitude': -3.689563, 'latitude': 40.358793, 'air_quality': None}, 
                                        {'longitude': -3.689457, 'latitude': 40.356724, 'air_quality': None}, 
                                        {'longitude': -3.689401, 'latitude': 40.356672, 'air_quality': None}, 
                                        {'longitude': -3.689415, 'latitude': 40.356605, 'air_quality': None}, 
                                        {'longitude': -3.689467, 'latitude': 40.356573, 'air_quality': None}, 
                                        {'longitude': -3.689417, 'latitude': 40.356039, 'air_quality': None}, 
                                        {'longitude': -3.689306, 'latitude': 40.354255, 'air_quality': None}, 
                                        {'longitude': -3.689252, 'latitude': 40.354199, 'air_quality': None}, 
                                        {'longitude': -3.688976, 'latitude': 40.354133, 'air_quality': None}, 
                                        {'longitude': -3.687736, 'latitude': 40.353203, 'air_quality': None}, 
                                        {'longitude': -3.687643, 'latitude': 40.353114, 'air_quality': None}, 
                                        {'longitude': -3.687616, 'latitude': 40.35307, 'air_quality': None}, 
                                        {'longitude': -3.68860, 'latitude': 40.35232, 'air_quality': None},
                                        {'longitude': -3.6887, 'latitude': 40.3521, 'air_quality': None}, 
                                        {'longitude': -3.6887, 'latitude': 40.3516, 'air_quality': None},
                                        {'longitude': -3.6884, 'latitude': 40.3504, 'air_quality': None},
                                        {'longitude': -3.6882, 'latitude': 40.3495, 'air_quality': None},
                                        {'longitude': -3.6879, 'latitude': 40.3485, 'air_quality': None},
                                        {'longitude': -3.687984, 'latitude': 40.347185, 'air_quality': None}, 
                                        {'longitude': -3.687923, 'latitude': 40.347064, 'air_quality': None}, 
                                        {'longitude': -3.688401, 'latitude': 40.346931, 'air_quality': None}, 
                                        {'longitude': -3.688857, 'latitude': 40.346834, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 14')


    def evaluation15(self):
        AirStation.objects.create(id = 1, name = 'TestAirStation1', latitude = 40.3858, longitude = -3.7129, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 2, name = 'TestAirStation2', latitude = 40.3858, longitude = -3.7041, messures = None, air_quality = 5, town_id = 79)
        AirStation.objects.create(id = 3, name = 'TestAirStation3', latitude = 40.3791, longitude = -3.7129, messures = None, air_quality = 1, town_id = 79)
        AirStation.objects.create(id = 4, name = 'TestAirStation4', latitude = 40.3791, longitude = -3.7041, messures = None, air_quality = 5, town_id = 79)

        response = self.client.post(self.index_url, {
            'initLatitude': 40.38248, 
            'initLongitude': -3.71732,
            'endLatitude': 40.38248,
            'endLongitude': -3.6996,
            'variation': 20
        })

        obtained_route = response.context['routes'][0]

        optimal_route = Route(nodes =   [{'longitude': -3.717326, 'latitude': 40.382481, 'air_quality': None}, 
                                        {'longitude': -3.717006, 'latitude': 40.383259, 'air_quality': None}, 
                                        {'longitude': -3.716942, 'latitude': 40.383298, 'air_quality': None}, 
                                        {'longitude': -3.716884, 'latitude': 40.383312, 'air_quality': None}, 
                                        {'longitude': -3.716814, 'latitude': 40.383311, 'air_quality': None}, 
                                        {'longitude': -3.715778, 'latitude': 40.383092, 'air_quality': None}, 
                                        {'longitude': -3.715639, 'latitude': 40.383044, 'air_quality': None}, 
                                        {'longitude': -3.715207, 'latitude': 40.382742, 'air_quality': None}, 
                                        {'longitude': -3.715141, 'latitude': 40.382631, 'air_quality': None}, 
                                        {'longitude': -3.713886, 'latitude': 40.382646, 'air_quality': None}, 
                                        {'longitude': -3.713392, 'latitude': 40.382669, 'air_quality': None}, 
                                        {'longitude': -3.713132, 'latitude': 40.382663, 'air_quality': None}, 
                                        {'longitude': -3.711253, 'latitude': 40.382699, 'air_quality': None}, 
                                        {'longitude': -3.708931, 'latitude': 40.382955, 'air_quality': None}, 
                                        {'longitude': -3.707763, 'latitude': 40.383066, 'air_quality': None}, 
                                        {'longitude': -3.706459, 'latitude': 40.383218, 'air_quality': None}, 
                                        {'longitude': -3.70356, 'latitude': 40.383518, 'air_quality': None}, 
                                        {'longitude': -3.7034, 'latitude': 40.383502, 'air_quality': None}, 
                                        {'longitude': -3.703003, 'latitude': 40.383409, 'air_quality': None}, 
                                        {'longitude': -3.702361, 'latitude': 40.383226, 'air_quality': None}, 
                                        {'longitude': -3.701468, 'latitude': 40.383076, 'air_quality': None}, 
                                        {'longitude': -3.699726, 'latitude': 40.383259, 'air_quality': None}, 
                                        {'longitude': -3.699603, 'latitude': 40.38248, 'air_quality': None}])

        get_results(self.threshold_failure, optimal_route, obtained_route, 'Evaluacion 15')
