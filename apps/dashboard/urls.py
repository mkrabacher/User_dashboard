from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^success/$', views.success),
    url(r'^all/$', views.showAll),
    url(r'^createPost/$', views.createPost),
    url(r'^createPost/$', views.createPost),
    url(r'^createComment/$', views.createComment),
    url(r'^show/(?P<number>\d+)$', views.show),
]