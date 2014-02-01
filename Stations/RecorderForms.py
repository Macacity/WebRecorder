# -*- encoding: utf-8 -*-
__author__ = 'TJ'

from django import forms
from Stations.models import Station, StreamType


class MainFormAudio(forms.Form):
    a = (StreamType.objects.filter(id=2)[0])
    audio = Station.objects.filter(streamType=a)

    station = forms.ModelChoiceField(queryset=audio, label="Audio Station",
                                     widget=forms.Select(attrs={
                                         'onclick': 'javascript:change(this.options[this.selectedIndex].text)'}))

    n = ''
    if audio:
        n = audio[0].name

    name = forms.CharField(max_length=45, initial=n, label="Name")
    timestamp = forms.BooleanField(initial=True, required=False)

    dauer = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'placeholder': 'HH:MM:SS, MM:SS or S',
                                                                        }))
    kapiteldauer = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Minuten', }))




class MainFormVideo(forms.Form):


    v = (StreamType.objects.filter(id=1)[0])
    video = Station.objects.filter(streamType=v)


    station = forms.ModelChoiceField(queryset=video, label="Video Station",
                                     widget=forms.Select(attrs={
                                         'onclick': 'javascript:change(this.options[this.selectedIndex].text)'}))
    n = ''
    if video:
        n = video[0].name
    name = forms.CharField(max_length=45, initial=n)
    timestamp = forms.BooleanField(initial=True, required=False)

    dauer = forms.CharField(max_length=8)


class newstationform(forms.Form):

    name = forms.CharField(max_length=45)
    urlstring = forms.CharField(max_length=500)
    typ = forms.ChoiceField(choices=(('Audio', 'Audio'), ('Video', 'Video')))
    kodierung = forms.CharField(max_length=5)


class taggform(forms.Form):
    titel = forms.CharField(max_length=50, required=False)
    albums = forms.CharField(max_length=50, required=False)
    kuenstler = forms.CharField(max_length=50, required=False, label="Kuenstler")

    jahr = forms.CharField(max_length=50, required=False)
    herausgeber = forms.CharField(max_length=50, required=False)
    titelnummer = forms.CharField(max_length=50, required=False)