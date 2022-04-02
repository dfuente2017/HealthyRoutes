from django.test import TestCase, Client
from django.urls import reverse
from users.models import User


# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = '/login/'
        self.register_url = '/register/'
        self.logout_url = '/logout/'
        self.profile_url = '/profile/'

        User.objects.create_user(email = 'testing@testing.com', password = 'Testing12345', nick = 'testing')
    

    #Login
    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


    def test_login_POST_user_login(self):
        response = self.client.post(self.login_url,{
            'email':'testing@testing.com',
            'pwd': 'Testing12345'
        }, follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(response.context['user'].is_active, True)


    def test_login_POST_inexistent_user(self):
        response = self.client.post(self.login_url, {
            'email':'inventeduser@inventeduser.com',
            'pwd':'Testing12345'
        }, follow = True)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals('message' in response.context, True)


    def test_login_POST_wrong_password(self):
        response = self.client.post(self.login_url, {
            'email':'testing@testing.com',
            'pwd':'wrongpassword'
        }, follow = True)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals('message' in response.context, True)