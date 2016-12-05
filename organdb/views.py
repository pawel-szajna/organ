from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.http import Http404
from itertools import groupby
import markdown
import datetime
import re

from .models import *
from .forms import *


def linkify(markdown, target_view, target_class):
    """
    Enables wikipedia-style linking.

    :param markdown: input markdown text
    :param target_view: URL name for link target
    :param target_class: model for link target (searching by name field)
    :return: markdown with generated links
    """
    def generate_link(matchobj):
        stop_name = matchobj.group(0)[2:-2]
        try:
            return '[' + stop_name + '](' + reverse(target_view, None, [target_class.objects.get(name__iexact=stop_name).pk]) + ')'
        except:
            return stop_name

    return re.sub(r'\[\[(.*?)\]\]', generate_link, markdown)


def instruments(request, description, instruments, search_form, message = None):
    """
    A list of instruments, usually used for search results. Responsible for sorting the data.

    :param request: the request
    :param description: a title for the page
    :param instruments: a QuerySet of instruments to include
    :param search_form: a search form or False if no form is to be displayed
    :return:
    """
    orderings = {
        'c': 'location__city__name',
        'l': 'location__name',
        'r': 'location__city__region__name',
        's': '-stops',
        'k': 'keyboards',
    }

    if request.GET.get('o') in orderings:
        instruments = instruments.order_by(orderings[request.GET.get('o')])

    return render(request, 'results.html', {
        'description': description,
        'search_form': search_form,
        'instruments': instruments,
        'message': message,
    })


# The views

def index(request):
    instruments = list(Instrument.objects.order_by('-pk')[:6])
    concerts = list(Concert.objects.filter(date__gte=datetime.datetime.now())[:6])
    stops = list(StopType.objects.order_by('?')[:6])

    return render(request, 'index.html', {
        'instruments': instruments,
        'concerts': concerts,
        'stops': stops
    })


@cache_page(60 * 60)
def instrument(request, instrument_id):
    try:
        the_instrument = Instrument.objects\
            .select_related('builder', 'location', 'location__city', 'location__city__region')\
            .prefetch_related('keyboard_set', 'keyboard_set__stop_set', 'recording_set', 'recording_set__performer')\
            .get(pk=instrument_id)
    except Instrument.DoesNotExist:
        raise Http404()

    description = markdown.markdown(the_instrument.description)
    additional = markdown.markdown(the_instrument.additional_features.replace('\n', '\n\n'))
    works = list(Work.objects.prefetch_related('builder').order_by('-year').filter(instrument=instrument_id))
    concerts = list(Concert.objects.filter(instrument=instrument_id, date__gte=datetime.datetime.now()))
    column_count = 4 if the_instrument.keyboards == 3 and the_instrument.pedalboard else 3
    column_size = 3 if column_count == 4 else 4

    return render(request, 'instrument.html', {
        'instrument': the_instrument,
        'concerts': concerts,
        'description': description,
        'additional': additional,
        'column_count': column_count,
        'column_size': column_size,
        'works': works,
    })


def stop_type(request, stop_type_id):
    the_stop_type = get_object_or_404(StopType, pk=stop_type_id)
    description = markdown.markdown(linkify(the_stop_type.description, 'view-stop-type', StopType))
    examples = list(Stop.objects.select_related('keyboard__instrument__location__city').filter(type=the_stop_type.pk).order_by('?')[:6])

    return render(request, 'stop.html', {
        'stop_type': the_stop_type,
        'description': description,
        'examples': examples,
    })


def performer(request, performer_id):
    the_performer = get_object_or_404(Performer, pk=performer_id)
    biography = markdown.markdown(the_performer.biography)

    return render(request, 'performer.html', {
        'performer': the_performer,
        'biography': biography,
    })


def performers(request):
    all_performers = get_list_or_404(Performer)
    the_performers = []

    for key, group in groupby(all_performers, lambda x: x.name[0]):
        the_performers.append([key, list(group)])

    return render(request, 'performers.html', {
        'performers': the_performers,
    })


def concert(request, concert_id):
    the_concert = get_object_or_404(Concert, pk=concert_id)
    description = markdown.markdown(the_concert.description)

    return render(request, 'concert.html', {
        'concert': the_concert,
        'description': description,
    })


def region(request, region_id):
    the_region = get_object_or_404(Region, pk=region_id)
    instrs = Instrument.objects.filter(location__city__region=the_region)

    return instruments(request, "województwo {}".format(the_region.name), instrs, False)


@cache_page(7 * 24 * 60 * 60)
def browse(request):
    regions = get_list_or_404(Region)

    return render(request, 'browse.html', {
        'regions': regions,
    })


def work(request, work_id):
    the_work = get_object_or_404(Work, pk=work_id)
    description = markdown.markdown(the_work.description)

    return render(request, 'work.html', {
        'work': the_work,
        'description': description,
    })


def builder(request, builder_id):
    the_builder = get_object_or_404(Builder, pk=builder_id)
    biography = markdown.markdown(the_builder.biography)

    return render(request, 'builder.html', {
        'builder': the_builder,
        'biography': biography,
    })


def builders(request):
    all_builders = list(Builder.objects.all())
    the_builders = []

    for key, group in groupby(all_builders, lambda x: x.name[0]):
        the_builders.append([key, list(group)])

    return render(request, 'builders.html', {
        'builders': the_builders,
    })


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

    return render(request, 'concerts.html', {
        'concerts': the_concerts,
    })


def family(request, family_id):
    the_family = get_object_or_404(StopFamily, pk=family_id)
    description = markdown.markdown(linkify(the_family.description, 'view-family', StopFamily))
    families = list(StopFamily.objects.all())

    if the_family.stoptype_set.count() > 7:
        stops = []
        for key, group in groupby(list(the_family.stoptype_set.all()), lambda x: x.name[0]):
            stops.append([key, list(group)])
    else:
        stops = False

    return render(request, 'stops.html', {
        'family': the_family,
        'description': description,
        'families': families,
        'stops': stops,
    })


def stops(request):
    all_stops = list(StopType.objects.all())
    the_families = get_list_or_404(StopFamily)
    the_stops = []

    for key, group in groupby(all_stops, lambda x: x.name[0]):
        the_stops.append([key, list(group)])

    return render(request, 'stops.html', {
        'stops': the_stops,
        'families': the_families,
    })


def search(request):
    message = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            instrs = Instrument.objects

            city = form.cleaned_data['city']
            location = form.cleaned_data['location']
            keyboards = form.cleaned_data['keyboards']
            pedalboard = form.cleaned_data['pedalboard']
            stops_min = form.cleaned_data['stops_min']
            stops_max = form.cleaned_data['stops_max']
            key_action = form.cleaned_data['key_action']
            stop_action = form.cleaned_data['stop_action']

            if not (city or location or keyboards or pedalboard != 'b' or stops_min or stops_max
                    or key_action != 'b' or stop_action != 'b'):
                instrs = False
                message = 'Proszę wypełnić przynajmniej jedno kryterium wyszukiwania.'
            else:
                if city:
                    instrs = instrs.filter(location__city__name__icontains=city)
                if location:
                    instrs = instrs.filter(location__name__icontains=location)
                if keyboards:
                    instrs = instrs.filter(keyboards=keyboards)
                if pedalboard != 'b':
                    instrs = instrs.filter(pedalboard=(pedalboard == 'y'))
                if stops_min:
                    instrs = instrs.filter(stops__gte=stops_min)
                if stops_max:
                    instrs = instrs.filter(stops__lte=stops_max)
                if key_action != 'b':
                    instrs = instrs.filter(key_action=key_action)
                if stop_action != 'b':
                    instrs = instrs.filter(stop_action=stop_action)

                if instrs.count() == 0:
                    message = 'Nie znaleziono instrumentów dla wybranych kryteriów.'
                    instrs = False

        else:
            message = 'Proszę poprawić błędy w formularzu.'
            instrs = False

    else:
        form = SearchForm(initial={'pedalboard': 'b'})
        instrs = False

    return instruments(request, 'wyszukiwanie', instrs, form, message)
