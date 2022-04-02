from audioop import reverse
import email
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from users.models import User

# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
    
    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)

    def test_login_POST_user_login(self):
        user = User.objects.create(email = 'testing@testing.com', password = 'Testing12345', nick = 'testing')

        response = self.client.post(self.login_url,{
            'email':'testing@testing.com',
            'pwd': 'Testing12345'
        })

        self.assertEquals(response.status_code, 302) #It is a redirection
        self.assertEquals(user, response.request.user)