from urllib import response
from django.test import TestCase, Client
from django.conf import settings
from air_stations.models import AirStation
from routes.models import Route
from users.models import User
from routes.services.GenerateTestingDataFunctions import generate_routes_testing_data

# Create your tests here.
class RoutesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = '/'
        self.saved_routes_url = '/saved-routes/'
        self.api_route = '/api/route'
        
        #User.objects.create_user(email = 'othertestinguser@othertestinguser.com', password = 'Testing12345', nick = 'othertestinguser')
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
        self.assertEquals(response.context['routes'].count(), 6)
        self.assertEquals(response.context['routes'].first().time, 2)
        self.assertEquals(response.context['routes'].last().time, 3)


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
        self.assertEquals(response.context['routes'].count(), 6)

        print(response.context['routes'][0].distance)
        print(response.context['routes'][1].distance)
        print(response.context['routes'][2].distance)
        print(response.context['routes'][3].distance)
        print(response.context['routes'][4].distance)
        print(response.context['routes'][5].distance)

        self.assertEquals(response.context['routes'].first().time, 4)
        self.assertEquals(response.context['routes'].last().time, 5)