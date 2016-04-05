from django.conf.urls.defaults import patterns,url
#from views import *

urlpatterns = patterns('',
    url(r'^$', 'SMSpoll.login.views.home'),
    url(r'^login/', 'SMSpoll.login.views.login'),
    url(r'^logout/', 'SMSpoll.login.views.logout', name='logout'),
    url(r'^signup/', 'SMSpoll.login.views.signup'),
    url(r'^contact-us/', 'SMSpoll.login.views.contact_us'),
    url(r'^login-check/', 'SMSpoll.login.views.login_check'),
    url(r'^recoverpswd/', 'SMSpoll.login.views.recover_pswd'),
    url(r'^attendance-string/', 'SMSpoll.login.views.attendace_string'),
    url(r'^after-course/', 'SMSpoll.login.views.after_course'),
    url(r'^add-remove/add', 'SMSpoll.login.views.add_course'),
    url(r'^add-remove/remove', 'SMSpoll.login.views.remove_course'),
    url(r'^add-remove/', 'SMSpoll.login.views.addrem'),
    url(r'^addQ/', 'SMSpoll.login.views.add_question'),
    url(r'^create-test/', 'SMSpoll.login.views.create_test'),
    url(r'^student-register/', 'SMSpoll.login.views.student_reg'),
    url(r'^conduct/', 'SMSpoll.login.views.conduct_test'),
    url(r'^show-stats/', 'SMSpoll.login.views.show_stats'),
    url(r'^download/', 'SMSpoll.login.views.download'),
    url(r'^show-attendance/', 'SMSpoll.login.views.show_attendance'),
    url(r'^download-attendance/', 'SMSpoll.login.views.download_attendance'),
    url(r'^like_category/$', 'SMSpoll.login.views.like_category', name='like_category'),

)