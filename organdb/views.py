from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import *


def index(request):
    return render(request, 'index.html', {})


def instrument(request, instrument_id):
    the_instrument = get_object_or_404(Instrument, pk=instrument_id)
    return render(request, 'instrument.html', {'instrument': the_instrument})


def stop_type(request, stop_type_id):
    the_stop_type = get_object_or_404(StopType, pk=stop_type_id)
    return render(request, 'stop.html', {'stop_type': the_stop_type})


def performer(request, performer_id):
    the_performer = get_object_or_404(Performer, pk=performer_id)
    return render(request, 'performer.html', {'performer': the_performer})


def concert(request, concert_id):
    the_concert = get_object_or_404(Concert, pk=concert_id)
    return render(request, 'concert.html', {'concert': the_concert})
