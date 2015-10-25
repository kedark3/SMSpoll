from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('',
    url(r'^$', 'SMSpoll.login.views.home', name='home'),
    url(r'^login/', 'SMSpoll.login.views.login'),
)