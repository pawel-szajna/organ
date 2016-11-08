from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^instrument/(?P<instrument_id>[0-9]+)', views.instrument, name='view-instrument'),
    url(r'^stop/(?P<stop_type_id>[0-9]+)', views.stop_type, name='view-stop-type'),
    #url(r'^performer/(?P<id>[0-9]+)', views.performer),
]
