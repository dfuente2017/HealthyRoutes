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
        self.api_get_air_stations_url = 'api/air_stations'

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
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_upload_air_stations_GET_with_no_superuser_logged(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.get(self.upload_air_stations_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'index.html')
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
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_upload_air_stations_POST_with_no_superuser_logged(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.upload_air_stations_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'index.html')
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
        self.assertEquals(AirStation.objects.first().id, 28079004)
        self.assertEquals(AirStation.objects.last().id, 28079060)


    #get_provinces
    def test_get_provinces_GET_with_no_user_logged(self):
        response = self.client.post(self.get_provinces_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_get_provinces_GET_with_no_superuser_logged(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.get_provinces_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'index.html')
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
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(response.context['user'].is_active, False)

    
    def test_get_towns_GET_with_no_superuser(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.get_towns_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'index.html')
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
