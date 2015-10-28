"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase,Client
from models import InstReg


class PollsViewsTestCase(TestCase):
    def test_login(self):
        resp = self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/login/')
        self.assertEqual(resp.status_code, 200)
    def test_home(self):
        resp = self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/')
        self.assertEqual(resp.status_code, 200)


    def test_signup(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/signup/', {'fname': 'fred','lname':'flinstone','email':'fred@gmail.com', 'pswd': 'secret','cnfm_pswd':'secret'})

        self.assertEqual(response.status_code, 200)
    def test_login_check_valid(self):
        instance = InstReg.objects.create(fname="kedar",lname="Kulkarni",email="kedar.kulkarni0@gmail.com",password="secret")
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/login-check/', {'email2':instance.email, 'pswd2': instance.password})

        self.assertEqual(response.status_code, 302) #Check this later again+++++++++++++++++++++++++++++++++++++++++++++++++++=
    def test_login_check_invalid(self):
        instance = InstReg.objects.create(fname="kedar",lname="Kulkarni",email="kedar.kulkarni0@gmail.com",password="secret")
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/login-check/', {'email2':instance.email, 'pswd2': 'abcd'})

        self.assertEqual(response.status_code, 200) #Check this later again+++++++++++++++++++++++++++++++++++++++++++++++++++=