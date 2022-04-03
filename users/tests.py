from django.test import TestCase, Client
from users.models import User
from os import remove
from django.conf import settings

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

    
    #Profile
    def test_profile_GET_with_logged_user(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.get(self.profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['user'].is_active, True)

    
    def test_profile_GET_without_logged_user(self):
        response = self.client.get(self.profile_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)
    

    def test_profile_POST_without_logged_user(self):
        response = self.client.post(self.profile_url)

        self.assertEquals(response.status_code, 401)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['user'].is_active, False)
    

    def test_profile_POST_no_upload_img(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['user'].user_img, '')

    
    def test_profile_POST_upload_img(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.profile_url)
        self.assertEquals(response.context['user'].user_img, '')

        img = open(str(settings.MEDIA_ROOT + 'user_img/users-testing-img.jpg').replace("\\","/"),'rb')
        
        response = self.client.post(self.profile_url,{
            'user_img':img
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['user'].user_img, 'user_img/testing.jpg')
        
        remove(str(settings.MEDIA_ROOT + 'user_img/testing.jpg').replace("\\","/"))

    def test_profile_POST_no_delete_img(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.profile_url,{
            'delete-img':'false'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertNotEquals(response.context['user'].user_img, None)

        response = self.client.post(self.profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertNotEquals(response.context['user'].user_img, None)


    def test_profile_POST_delete_img(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')

        response = self.client.post(self.profile_url,{
            'delete-img':'true'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(response.context['user'].user_img, '')

    
    def test_profile_POST_different_passwords(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.profile_url,{
            'pwd1':'Testing12345',
            'pwd2': '12345Testing'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_pwd' in response.context, True)
        self.assertEquals(self.client.login(username = 'testing@testing.com', password = 'Testing12345'), True)#Check that the password didn't change


    def test_profile_POST_short_password(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.profile_url,{
            'pwd1':'Testing',
            'pwd2': 'Testing'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_pwd' in response.context, True)
        self.assertEquals(self.client.login(username = 'testing@testing.com', password = 'Testing12345'), True)


    def test_register_POST_no_lower_case_letter_in_password(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.profile_url,{
            'pwd1':'TESTING12345',
            'pwd2':'TESTING12345'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_pwd' in response.context, True)
        self.assertEquals(self.client.login(username = 'testing@testing.com', password = 'Testing12345'), True)

    
    def test_register_POST_no_upper_case_letter_in_password(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.profile_url,{
            'pwd1':'testing12345',
            'pwd2':'testing12345'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_pwd' in response.context, True)
        self.assertEquals(self.client.login(username = 'testing@testing.com', password = 'Testing12345'), True)


    def test_register_POST_no_number_in_password(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.profile_url,{
            'pwd1':'TestingTesting',
            'pwd2':'TestingTesting'
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_pwd' in response.context, True)
        self.assertEquals(self.client.login(username = 'testing@testing.com', password = 'Testing12345'), True)


    def test_resgister_POST_password_changed_succesfully(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.profile_url,{
            'pwd1':'12345Testing',
            'pwd2':'12345Testing'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_pwd' in response.context, False)
        self.assertEquals(self.client.login(username = 'testing@testing.com', password = 'Testing12345'), False)
        self.assertEquals(self.client.login(username = 'testing@testing.com', password = '12345Testing'), True)


    def test_register_POST_used_nick(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        User.objects.create_user(email='registeremail@registeremail.com', password='Testing12345', nick='registeremail').save()

        response = self.client.post(self.profile_url,{
            'nick':'registeremail',
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_nick' in response.context, True)
        self.assertEquals(response.context['user'].nick, 'testing')
        self.assertNotEquals(response.context['user'].nick, 'registeremail')

    
    def test_register_POST_unuser_nick(self):
        self.client.login(username = 'testing@testing.com', password = 'Testing12345')
        
        response = self.client.post(self.profile_url,{
            'nick':'Testing',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals('message_nick' in response.context, False)
        self.assertEquals(response.context['user'].nick, 'Testing')
        self.assertNotEquals(response.context['user'].nick, 'testing')