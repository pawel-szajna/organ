from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index),

    # Instruments library
    url(r'^search/', views.search, name='view-search'),
    url(r'^browse/', views.browse, name='view-browse'),
    url(r'^region/(?P<region_id>[0-9]+)', views.region, name='view-region'),
    url(r'^instrument/(?P<instrument_id>[0-9]+)', views.instrument, name='view-instrument'),
    url(r'^work/(?P<work_id>[0-9]+)', views.work, name='view-work'),
    url(r'^builder/(?P<builder_id>[0-9]+)', views.builder, name='view-builder'),

    # Stops library
    url(r'^stops/', views.stops, name='view-stops'),
    url(r'^stop/(?P<stop_type_id>[0-9]+)', views.stop_type, name='view-stop-type'),
    url(r'^family/(?P<family_id>[0-9]+)', views.family, name='view-family'),

    # Concerts and performers library
    url(r'^concerts/', views.concerts, name='view-concerts'),
    url(r'^concert/(?P<concert_id>[0-9]+)', views.concert, name='view-concert'),
    url(r'^performer/(?P<performer_id>[0-9]+)', views.performer, name='view-performer'),

]
