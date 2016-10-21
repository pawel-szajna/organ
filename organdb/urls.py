from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^instrument/(?P<id>[0-9]+)', views.instrument),
]
