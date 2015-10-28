from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('',
    url(r'^$', 'SMSpoll.login.views.home', name='home'),
    url(r'^login/', 'SMSpoll.login.views.login'),
    url(r'^signup/', 'SMSpoll.login.views.signup'),
    url(r'^login-check/', 'SMSpoll.login.views.login_check'),
)