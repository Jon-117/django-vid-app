from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Video
from .forms import VideoForm, SearchForm
from django.db import IntegrityError
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError


# Create your views here.

def home(request):
    app_name = 'VidCollector'
    return render(request, 'video_collection/home.html', {'app_name':app_name})


def add(request):

    if request.method == 'POST':
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                # messages.info(request, 'Saved successfully!')
                return redirect(video_list)
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'Vid already collected')


        messages.warning(request, 'Invalid, check your input!')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})


def video_list(request):
    search_form = SearchForm(request.GET)  # build form from data user sends to app

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name'))
    else:
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))


    return render(request, 'video_collection/video_list.html', {'videos':videos, 'search_form': search_form})
