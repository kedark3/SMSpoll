"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from models import Course,InstReg


class PollsViewsTestCase(TestCase):
    def test_login(self):
        resp = self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/login/')
        self.assertEqual(resp.status_code, 200)
    def test_home(self):
        resp = self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/',{'email2':'kkulkar3@uncc.edu'})
        self.assertEqual(resp.status_code, 200)


    def test_signup_valid(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/signup/', {'fname': 'fred','lname':'flinstone','email':'fred@gmail.com', 'pswd': 'secret','cnfm_pswd':'secret'})

        self.assertEqual(response.status_code, 302)

    def test_signup_invalid(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/signup/', {'fname': 'fred','lname':'flinstone','email':'fred@gmail.com', 'pswd': 'secresst','cnfm_pswd':'secret'})

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

    def test_course_desc(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/after-course/', {'crn':21546, 'c-id': 6150})
        self.assertEqual(response.status_code, 200)


    def test_studreg_valid(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/student-register/', {'From': '+17049048709','Body':'800893339 1001'})
        self.assertEqual(response.status_code, 200)

    def test_studreg_invalid(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/student-register/', {'From': '+17049048709','Body':'800893339 ab 1001'})
        self.assertEqual(response.status_code, 200)

    def test_attendance_string_and_set_counter(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/attendance-string/', {'count':90})
        self.assertEqual(response.status_code, 200)

    def test_show_attendance(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/show-attendance/')
        self.assertEqual(response.status_code, 200)


    def test_download_attendance(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/download-attendance/')
        self.assertEqual(response.status_code, 200)

    '''def test_add_remove(self):
        instance = InstReg.objects.create(fname="Kedar",lname="Kulkarni",email="kedar.kulkarni0@gmail.com",password="secret")
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/login-check/', {'email2':instance.email, 'pswd2': instance.password})

        response=c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/add-remove/remove/',{'email':instance.email,'cid':1,'crn':1425})
        self.assertEqual(response.status_code, 302)
        response=c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/add-remove/add/',{'email':instance.email,'cid':1,'crn':2357})
        self.assertEqual(response.status_code, 302)
'''

