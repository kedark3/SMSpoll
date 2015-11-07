from django.conf.urls.defaults import patterns,url
#from views import *

urlpatterns = patterns('',
    url(r'^$', 'SMSpoll.login.views.home'),
    url(r'^login/', 'SMSpoll.login.views.login'),
    url(r'^signup/', 'SMSpoll.login.views.signup'),
    url(r'^contact-us/', 'SMSpoll.login.views.contact_us'),
    url(r'^login-check/', 'SMSpoll.login.views.login_check'),
    url(r'^recoverpswd/', 'SMSpoll.login.views.recover_pswd'),
    url(r'^attendance-string/', 'SMSpoll.login.views.attendace_string'),
    url(r'^after-course/', 'SMSpoll.login.views.after_course'),
    url(r'^student-register/', 'SMSpoll.login.views.student_reg'),
    url(r'^show-attendance/', 'SMSpoll.login.views.show_attendance'),
)