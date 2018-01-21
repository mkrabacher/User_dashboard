
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registerUser$', views.registerUser),
    url(r'^(?P<number>\d+)/edit$', views.edit),
    url(r'^register/$', views.register),
    url(r'^updateInfo/$', views.updateInfo),
    url(r'^signin/$', views.signin),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success)
]
