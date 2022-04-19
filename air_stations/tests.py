from django.conf import settings
from django.test import TestCase, Client
from users.models import User
from air_stations.models import Country, Province, Town, AirStation, Arguments
import json


# Create your tests here.
class AirStationsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_air_stations_url = '/upload-air-stations'
        self.get_provinces_url = '/get/provinces'
        self.get_towns_url = '/get/towns'
        self.api_get_air_stations_url = '/api/air_stations'

        User.objects.create_user(email = 'testing@testing.com', password = 'Testing12345', nick= 'testing')
        self.su = User.objects.create_superuser(email = 'testingsu@testing.com', password = 'Testing12345', nick = 'testingsu', is_admin = True, is_staff = True, is_superuser = True)
        Country.objects.create(id = 0, name = 'TestCountry')
        Province.objects.create(id = 28, name = 'TestProvince', country = 0)
        Town.objects.create(id = 79, name = 'TestTown', url = None, province = 28, last_modified = None)
        Arguments.objects.create(id = 1, town_id = 79, argument_type = 'ASD', arguments = [{'id':0, 'argument':'CODIGO'},{'id':1, 'argument':'ESTACION'},{'id':2, 'argument':'LONGITUD'},{'id':3, 'argument':'LATITUD'}])


    #upload_air_stations
    def test_upload_air_stations_GET_with_no_logged_user(self):
        response = self.client.get(self.upload_air_stations_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_upload_air_stations_GET_with_no_superuser_logged(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.get(self.upload_air_stations_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, True)


    def test_upload_air_stations_GET_with_superuser_logged(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        response = self.client.get(self.upload_air_stations_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload-air-stations.html')
        self.assertEquals(response.context['countries'][0], Country.objects.get(id = 0))

    
    def test_upload_air_stations_POST_with_no_logged_user(self):
        response = self.client.post(self.upload_air_stations_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_upload_air_stations_POST_with_no_superuser_logged(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.upload_air_stations_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals(response.context['user'].is_superuser, False)
    

    def test_upload_air_stations_POST_with_superuser_logged(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        csv = open(str(settings.MEDIA_ROOT + 'testing-files/test-stations-load.csv'))
        
        response = self.client.post(self.upload_air_stations_url,{
            'town':79,
            'town-stations-excel':csv
        }, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('upload-air-stations.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals(response.context['user'].is_superuser, True)

        self.assertEquals(AirStation.objects.count(), 24)

        self.assertAlmostEquals(AirStation.objects.first().id, 28079004)
        self.assertEquals(AirStation.objects.first().name, 'Pza. de EspaÃ±a')
        self.assertEquals(AirStation.objects.first().latitude, '40.423882300000002488')
        self.assertEquals(AirStation.objects.first().longitude, '-3.712256700000000187')
        self.assertEquals(AirStation.objects.first().town_id, 79)

        self.assertEquals(AirStation.objects.last().id, 28079060)
        self.assertEquals(AirStation.objects.last().name, 'Tres Olivos')
        self.assertEquals(AirStation.objects.last().latitude, '40.500547699999998486')
        self.assertEquals(AirStation.objects.last().longitude, '-3.689730799999999977')
        self.assertEquals(AirStation.objects.last().town_id, 79)


    #get_provinces
    def test_get_provinces_GET_with_no_user_logged(self):
        response = self.client.post(self.get_provinces_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_get_provinces_GET_with_no_superuser_logged(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.get_provinces_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals(response.context['user'].is_superuser, False)


    def test_get_provinces_GET_incorrect_country_id(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        response = self.client.get(self.get_provinces_url,{
            'country_id':1
        })

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error' in json.loads(response.content), True)


    def test_get_provinces_GET_correct_country_id(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        response = self.client.get(self.get_provinces_url,{
            'country_id':0
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content),{'28':'TestProvince'})



    def test_get_provinces_GET_no_country(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        response = self.client.get(self.get_provinces_url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error' in json.loads(response.content), True)  
    

    #get_towns
    def test_get_towns_GET_with_no_user_logged(self):
        response = self.client.post(self.get_towns_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)

    
    def test_get_towns_GET_with_no_superuser(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.get_towns_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, True)
        self.assertEquals(response.context['user'].is_superuser, False)

    
    def test_get_towns_GET_incorrect_province_id(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        response = self.client.get(self.get_towns_url,{
            'province_id':0
        })

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error' in json.loads(response.content), True)


    def test_get_towns_GET_correct_province_id(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        response = self.client.get(self.get_towns_url,{
            'province_id':28
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content),{'79':'TestTown'})


    def test_get_towns_GET_no_province(self):
        self.client.login(username = 'testingsu@testing.com', password = 'Testing12345')

        response = self.client.get(self.get_towns_url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals('error' in json.loads(response.content), True)


    #api_get_air_stations
    def test_api_get_air_stations_GET_incorrect_town_id(self):
        AirStation.objects.create(id= 1, name = 'TestAirStation1', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 2, name = 'TestAirStation2', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 3, name = 'TestAirStation3', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 4, name = 'TestAirStation4', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 5, name = 'TestAirStation5', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 6, name = 'TestAirStation6', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 80)#Object with other town_id

        response = self.client.get(self.api_get_air_stations_url,{
            'town_id':0
        })

        self.assertEquals(response.status_code,400)
        
    
    def test_api_get_air_stations_GET_correct_town_id(self):
        AirStation.objects.create(id= 1, name = 'TestAirStation1', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 2, name = 'TestAirStation2', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 3, name = 'TestAirStation3', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 4, name = 'TestAirStation4', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 5, name = 'TestAirStation5', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 6, name = 'TestAirStation6', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 80)#Object with other town_id

        response = self.client.get(self.api_get_air_stations_url,{
            'town_id':79
        })

        air_stations = json.loads(response.content)
        air_stations_db = AirStation.objects.filter(town_id = 79)
        air_stations_db_count = len(air_stations_db)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(air_stations_db[0].id, air_stations[0]['id'])
        self.assertEquals(air_stations_db[air_stations_db_count-1].id, air_stations[air_stations_db_count-1]['id'])


    def test_api_get_air_stations_GET_no_town_id(self):
        AirStation.objects.create(id= 1, name = 'TestAirStation1', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 2, name = 'TestAirStation2', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 3, name = 'TestAirStation3', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 4, name = 'TestAirStation4', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 5, name = 'TestAirStation5', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 79)
        AirStation.objects.create(id= 6, name = 'TestAirStation6', latitude = 40.01, longitude = -3.71, messures = None, air_quality = None, town_id = 80)#Object with other town_id

        response = self.client.get(self.api_get_air_stations_url)

        self.assertEquals(response.status_code, 400)