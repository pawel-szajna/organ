from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template import Context
from django.http import HttpResponse
import datetime

from .models import *


def index(request):
    instruments = list(Instrument.objects.order_by('-pk')[:6])
    concerts = list(Concert.objects.filter(date__gte=datetime.datetime.now())[:6])
    stops = list(StopType.objects.order_by('?')[:6])
    return render(request, 'index.html', {'instruments': instruments, 'concerts': concerts, 'stops': stops})


def instrument(request, instrument_id):
    the_instrument = get_object_or_404(Instrument, pk=instrument_id)
    concerts = list(Concert.objects.filter(instrument=instrument_id, date__gte=datetime.datetime.now()))
    return render(request, 'instrument.html', {'instrument': the_instrument, 'concerts': concerts})


def stop_type(request, stop_type_id):
    the_stop_type = get_object_or_404(StopType, pk=stop_type_id)
    return render(request, 'stop.html', {'stop_type': the_stop_type})


def performer(request, performer_id):
    the_performer = get_object_or_404(Performer, pk=performer_id)
    return render(request, 'performer.html', {'performer': the_performer})


def concert(request, concert_id):
    the_concert = get_object_or_404(Concert, pk=concert_id)
    return render(request, 'concert.html', {'concert': the_concert})


def region(request, region_id):
    the_region = get_object_or_404(Region, pk=region_id)
    return render(request, 'region.html', {'region': the_region})


def browse(request):
    regions = get_list_or_404(Region)
    return render(request, 'browse.html', {'regions': regions})


def work(request, work_id):
    the_work = get_object_or_404(Work, pk=work_id)
    return render(request, 'work.html', {'work': the_work})


def builder(request, builder_id):
    the_builder = get_object_or_404(Builder, pk=builder_id)
    return render(request, 'builder.html', {'builder': the_builder})


def concerts(request):
    regions = list(Region.objects.all())
    the_concerts = list()
    for region in regions:
        the_concerts.append({
            'region': region,
            'concerts': list(Concert.objects.filter(
                instrument__location__city__region__pk=region.pk,
                date__gte=datetime.datetime.now()
            ))
        })
    return render(request, 'concerts.html', {'concerts': the_concerts})


def family(request, family_id):
    the_family = get_object_or_404(StopFamily, pk=family_id)
    return render(request, 'family.html', {'family': the_family})


def search(request):
    return render(request, 'search.html', {})


def stops(request):
    the_stops = get_list_or_404(StopType)
    the_families = get_list_or_404(StopFamily)
    return render(request, 'stops.html', {'stops': the_stops, 'families': the_families})
