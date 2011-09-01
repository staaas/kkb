# -*- coding:utf-8 -*-
import os.path
import random
from datetime import timedelta, datetime

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.files.images import get_image_dimensions
from django.core.files.base import ContentFile, File
from social_auth.views import auth as social_auth_begin

from commonutils.decorators import render_to
from models import CinemaClubEvent, CinemaClub, TemporaryImage
from forms import CinemaClubEventForm, TemporaryImageForm, CropImageForm
from utils import crop_image

def kkb_socialauth_begin(request, backend):
    '''we want to logout before logging in as another user.'''
    auth_logout(request)
    return social_auth_begin(request, backend)

HOME_CINEMACLUBS_COUNT = 4
HOME_EVENTS_COUNT = 4

@render_to('cinemaclubs/bhome.html')
def minsk(request):
    upcoming_events = CinemaClubEvent.objects.filter(
        starts_at__gte=datetime.now() - timedelta(hours=1)).order_by(
        'starts_at')[:HOME_EVENTS_COUNT]
    cinemaclubs = list(CinemaClub.objects.all())

    return {'upcoming_events': upcoming_events,
            'cinemaclubs': random.sample(cinemaclubs,
                                         min(HOME_CINEMACLUBS_COUNT,
                                             len(cinemaclubs))),}


def home(request):
    return redirect('minsk', permanent=False)

@render_to('cinemaclubs/bcinemaclub_about.html')
def cinemaclub_about(request, cinemaclub_slug):
    cinemaclub = get_object_or_404(CinemaClub,
                                   slug=cinemaclub_slug)
    upcoming_cinemaclub_events = CinemaClubEvent.objects.filter(
        starts_at__gte=datetime.now() - timedelta(hours=1)).filter(
        organizer=cinemaclub).order_by('starts_at')
    return {'cinemaclub': cinemaclub,
            'upcoming_cinemaclub_events': upcoming_cinemaclub_events}


@render_to('cinemaclubs/bcinemaclubevent.html')
def cinemaclubevent(request, cinemaclub_slug, event_id):
    event = get_object_or_404(CinemaClubEvent,
                              id=event_id,
                              organizer__slug=cinemaclub_slug)

    return {'event': event}


@render_to('cinemaclubs/bcinemaclubevent.html')
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

@login_required
@render_to('cinemaclubs/cinemaclubevent_add.html')
def cinemaclubevent_add(request):
    if request.user.is_staff:
        cinemaclubs = list(CinemaClub.objects.all())
    else:
        cinemaclubs = list(request.user.cinemaclubs.all())

    if not cinemaclubs:
        return HttpResponse(status=403)

    form = CinemaClubEventForm(request.POST or None)
    form.base_fields['organizer'].choices = \
        [(c.id, c) for c in cinemaclubs]
    if form.is_valid():
        event = form.save(commit=False)
        event.save()
        return HttpResponseRedirect(reverse('cinemaclubevent_edit_poster',
                                            args=[event.id]))
    return {'form': form}
    
@login_required
@render_to('cinemaclubs/cinemaclubevent_edit_poster.html')
def cinemaclubevent_edit_poster(request, event_id):
    '''
    This view allows user to upload an event poster.
    If we have an appropriate poster, 
    '''
    if not request.user.is_staff and \
            event_id not in list(e.id for e in request.user.cinemaclubs.all()):
        raise Http404

    event = get_object_or_404(CinemaClubEvent,
                              id=event_id)

    if request.method == 'POST':
        form = TemporaryImageForm(request.POST, request.FILES)
        if form.is_valid():
            w, h = get_image_dimensions(form.cleaned_data.get('image'))
            tmp_img = form.save(commit=False)
            if w != h:
                tmp_img.uploaded_by = request.user
                tmp_img.save()
                return HttpResponseRedirect(
                    reverse('cinemaclubevent_crop_poster', args=[event_id,
                                                                 tmp_img.id]))
            event.poster.save(os.path.basename(unicode(tmp_img.image)),
                              File(tmp_img.image))
            return HttpResponseRedirect(
                reverse('someevent', args=[event_id]))
    else:
        form = TemporaryImageForm()

    return {'form': form,
            'event': event,}

@login_required
@render_to('cinemaclubs/cinemaclubevent_crop_poster.html')
def cinemaclubevent_crop_poster(request, event_id, tmp_img_id):
    if not request.user.is_staff and \
            event_id not in list(e.id for e in request.user.cinemaclubs.all()):
        raise Http404

    return object_crop_image(request, event_id, CinemaClubEvent,
                             'someevent', 'poster', tmp_img_id)

def object_crop_image(request, object_id, object_class,
                       object_details_view, object_image_field,
                       tmp_img_id):
    obj = get_object_or_404(object_class,
                              id=object_id)
    tmp_img = get_object_or_404(TemporaryImage,
                                id=tmp_img_id,
                                uploaded_by=request.user)
    width, height = get_image_dimensions(tmp_img.image)

    form = CropImageForm(width, height, request.POST or None)
    if form.is_valid():
        cropped_img = crop_image(tmp_img.image,
                                 form.cleaned_data['x1'],
                                 form.cleaned_data['y1'],
                                 form.cleaned_data['x2'],
                                 form.cleaned_data['y2'])
        getattr(obj, object_image_field).save(
            '%s.png' % os.path.basename(unicode(tmp_img.image)),
            ContentFile(cropped_img))
        return HttpResponseRedirect(
            reverse(object_details_view, args=[object_id]))

    return {'image_url': tmp_img.url,
            'selection_size': min(width, height),
            'form': form,}
