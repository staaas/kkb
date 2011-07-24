# -*- coding:utf-8 -*-
from datetime import timedelta, datetime
import random

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from commonutils.decorators import render_to
from models import CinemaClubEvent, CinemaClub


def chunks(some_list, chunk_size):
    return [some_list[i: i + chunk_size] for i in \
                xrange(0, len(some_list), chunk_size)]

HOME_CINEMACLUBS_COUNT = 4
HOME_EVENTS_COUNT = 4

@render_to('cinemaclubs/home.html')
def minsk(request):
    upcoming_events = CinemaClubEvent.objects.filter(
        starts_at__gte=datetime.now() - timedelta(hours=1)).order_by(
        'starts_at')[:HOME_EVENTS_COUNT]
    upcoming_events_chunks = chunks(list(upcoming_events), HOME_EVENTS_COUNT)
    cinemaclubs = list(CinemaClub.objects.all())

    return {'upcoming_events_chunks': upcoming_events_chunks,
            'cinemaclubs': random.sample(cinemaclubs,
                                         min(HOME_CINEMACLUBS_COUNT,
                                             len(cinemaclubs))),}


def home(request):
    return redirect('minsk', permanent=True)

@render_to('cinemaclubs/cinemaclub_about.html')
def cinemaclub_about(request, cinemaclub_slug):
    cinemaclub = get_object_or_404(CinemaClub,
                                   slug=cinemaclub_slug)
    upcoming_cinemaclub_events = CinemaClubEvent.objects.filter(
        starts_at__gte=datetime.now() - timedelta(hours=1)).filter(
        organizer=cinemaclub).order_by('starts_at')
    return {'cinemaclub': cinemaclub,
            'upcoming_cinemaclub_events': upcoming_cinemaclub_events}


@render_to('cinemaclubs/cinemaclubevent.html')
def cinemaclubevent(request, cinemaclub_slug, event_id):
    event = get_object_or_404(CinemaClubEvent,
                              id=event_id,
                              organizer__slug=cinemaclub_slug)

    return {'event': event}


@render_to('cinemaclubs/cinemaclubevent.html')
def someevent(request, event_id):
    event = get_object_or_404(CinemaClubEvent, id=event_id)
    if event.organizer:
        return redirect("cinemaclubevent", event.organizer.slug, event_id,
                        permanent=True)

    return {'event': event}

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('home')

def add_cinemaclubevent(request):
    pass
