from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
import datetime

from .models import *


def index(request):
    return render(request, 'index.html', {})


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
    return render(request, 'concerts.html', {})


def family(request, family_id):
    the_family = get_object_or_404(StopFamily, pk=family_id)
    return render(request, 'family.html', {'family': the_family})


def search(request):
    return render(request, 'search.html', {})
