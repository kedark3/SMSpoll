"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from django.test.client import Client
from models import InstReg
from django.conf import settings
from django.utils.importlib import import_module
from datetime import datetime
from django.utils import timezone


class PollsViewsTestCase(unittest.TestCase):
    def setUp(self):

        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module('django.contrib.sessions.backends.file')
        store = engine.SessionStore()
        store.save()

        self.client = Client()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key

    def test_login(self):
        resp = self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/login/')
        self.assertEqual(resp.status_code, 200)
    def test_home(self):
        resp = self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/',{'email2':'kkulkar3@uncc.edu'})
        self.assertEqual(resp.status_code, 200)


    def test_signup_valid(self):
        response=self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/signup/', {'fname': 'fred','lname':'flinstone','email':'fred@gmail.com', 'pswd': 'secret','cnfm_pswd':'secret'})
        self.assertEqual(response.status_code, 302)

    def test_signup_invalid(self):

        response=self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/signup/', {'fname': 'fred','lname':'flinstone','email':'fred@gmail.com', 'pswd': 'secresst','cnfm_pswd':'secret'})

        self.assertEqual(response.status_code, 200)


    def test_login_check_valid(self):
        instance = InstReg.objects.create(fname="kedar",lname="Kulkarni",email="kedar.kulkarni0@gmail.com",password="secret")

        response=self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/login-check/', {'email2':instance.email, 'pswd2': instance.password})

        self.assertEqual(response.status_code, 302)
    def test_login_check_invalid(self):
        response=self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/login-check/',{'email2':'g@mail.com', 'pswd2': 'abcd'})
        self.assertEqual(response.status_code, 200)

    def test_course_desc(self):
        response=self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/after-course/', {'crn':21546, 'c-id': 6150})
        self.assertEqual(response.status_code, 200)


    def test_studreg_valid(self):
        response=self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/student-register/', {'From': '+17049048709','Body':'800893339 1001'})
        self.assertEqual(response.status_code, 200)

    def test_studreg_invalid(self):
        response=self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/student-register/', {'From': '+17049048709','Body':'800893339 ab 1001'})
        self.assertEqual(response.status_code, 200)

    def test_attendance_string_and_set_counter(self):

        response=self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/attendance-string/', {'count':90})
        self.assertEqual(response.status_code, 200)

    def test_show_attendance(self):

        session = self.session
        session['count'] = '90'
        session['random_string']='abcde'
        session.save()
        response=self.client.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/show-attendance/')
        self.assertEqual(response.status_code, 200)


    def test_download_attendance(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/download-attendance/')
        self.assertEqual(response.status_code, 200)

    def test_create_test_successful(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/create-test/',{'test_id':'Test1','crn':23153,'cid':6112, 'qid':1})
        self.assertEqual(response.status_code, 200)

    def test_add_question_successful(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/addQ/',{'crn':23153, 'question':'Is flower a living thing?', 'A':'Yes', 'B':'No', 'C':'NA', 'D':'NA', 'correct':'A', 'timer':10, 'qid':1, 'test_id':'Test1'})
        self.assertEqual(response.status_code, 302)

    def test_conduct_test_successful(self):
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/conduct/',{'qid':1, 'test_id':'Test1', 'crn':23153})
        self.assertEqual(response.status_code, 200)
    def test_show_stats(self):
        session = self.client.session
        session['test_id'] = 'test'
        session['timer']=10
        session.save()
        response = self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/show-stats/',{'qid':1,'crn':23153})
        self.assertEqual(response.status_code, 200)

    def test_download(self):
        response = self.client.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/download/',{'test_id':'Test1', 'crn':23153})
        self.assertEqual(response.status_code, 302)













'''
    def test_conduct_test_unsuccessful(self):           #fails when crn is not found!
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/conduct/',{'qid':10, 'test_id':'Test1', 'crn':2353})
        self.assertEqual(response.status_code, 302)'''
'''
    def test_add_remove(self):
        instance = InstReg.objects.create(fname="Kedar",lname="Kulkarni",email="kedar.kulkarni0@gmail.com",password="secret")
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response=c.post('http://ssdiprojectfall2015.pythonanywhere.com/auth/login-check/', {'email2':instance.email, 'pswd2': instance.password})

        response=c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/add-remove/remove/',{'email':instance.email,'cid':1,'crn':1425})
        self.assertEqual(response.status_code, 302)
        response=c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/add-remove/add/',{'email':instance.email,'cid':1,'crn':2357})
        self.assertEqual(response.status_code, 302)
'''

'''def test_create_test_unsuccessful(self):        #fails when crn is not found!
        c = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = c.get('http://ssdiprojectfall2015.pythonanywhere.com/auth/create-test/',{'test_id':'Tes','crn':253,'cid':6112, 'qid':1})
        self.assertEqual(response.status_code, 200)
'''