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

    
    #Register
    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


    def test_register_POST_different_passwords(self):
        response = self.client.post(self.register_url, {
            'email':'registeremail@registeremail.com',
            'nick':'registeremail',
            'pwd1':'Testing12345',
            'pwd2':'12345Testing'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'register.html')
        self.assertEquals('message_pwd' in response.context, True)
    

    def test_register_POST_short_password(self):
        response = self.client.post(self.register_url, {
            'email':'registeremail@registeremail.com',
            'nick':'registeremail',
            'pwd1':'Testing',
            'pwd2':'Testing'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'register.html')
        self.assertEquals('message_pwd' in response.context, True)
    

    def test_register_POST_no_lower_case_letter_in_password(self):
        response = self.client.post(self.register_url, {
            'email':'registeremail@registeremail.com',
            'nick':'registeremail',
            'pwd1':'TESTING12345',
            'pwd2':'TESTING12345'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'register.html')
        self.assertEquals('message_pwd' in response.context, True)


    def test_register_POST_no_upper_case_letter_in_password(self):
        response = self.client.post(self.register_url, {
            'email':'registeremail@registeremail.com',
            'nick':'registeremail',
            'pwd1':'testing12345',
            'pwd2':'testing12345'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'register.html')
        self.assertEquals('message_pwd' in response.context, True)

    
    def test_register_POST_no_number_in_password(self):
        response = self.client.post(self.register_url, {
            'email':'registeremail@registeremail.com',
            'nick':'registeremail',
            'pwd1':'TestingTesting',
            'pwd2':'TestingTesting'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'register.html')
        self.assertEquals('message_pwd' in response.context, True)


    def test_register_POST_used_email(self):
        response = self.client.post(self.register_url, {
            'email':'testing@testing.com',
            'nick':'registeremail',
            'pwd1':'Testing12345',
            'pwd2':'Testing12345'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'register.html')
        self.assertEquals('message_email' in response.context, True)


    def test_register_POST_used_nick(self):
        response = self.client.post(self.register_url, {
            'email':'registeremail@registeremail.com',
            'nick':'testing',
            'pwd1':'Testing12345',
            'pwd2':'Testing12345'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'register.html')
        self.assertEquals('message_nick' in response.context, True)


    def test_register_POST_correct_register(self):
        response = self.client.post(self.register_url, {
            'email':'registeremail@registeremail.com',
            'nick':'registeremail',
            'pwd1':'Testing12345',
            'pwd2':'Testing12345'
        }, follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals('message_pwd' in response.context, False)
        self.assertEquals('message_email' in response.context, False)
        self.assertEquals('message_nick' in response.context, False)


    #Logout
    def test_logout_with_logged_user(self):
        response = self.client.post(self.login_url,{
            'email':'testing@testing.com',
            'pwd': 'Testing12345'
        }, follow = True)

        self.assertEquals(response.context['user'].is_active, True)
        
        response = self.client.get(self.logout_url, follow = True)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(response.context['user'].is_active, False)


    def test_logout_without_logged_user(self):
        response = self.client.get(self.login_url)
        
        self.assertEquals(response.context['user'].is_active, False)
        
        response = self.client.get(self.logout_url, follow = True)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(response.context['user'].is_active, False)