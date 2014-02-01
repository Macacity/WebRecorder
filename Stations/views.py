# -*- encoding: utf-8 -*-
# Create your views here.
import os
import threading
from django.http import HttpResponseRedirect, Http404, HttpResponse
from Stations.Recorder import video_recorder, audio_recorder
from Stations.RecorderForms import MainFormAudio, MainFormVideo, newstationform, taggform
from Stations.models import StreamType, Station
from django.shortcuts import render
from mp3_tagger import mp3tagger


BASEDIR = os.path.dirname(os.path.abspath(__file__))


def getStations(request):
    audiostreams = (StreamType.objects.filter(stream_type="Audio")[0])
    audio = Station.objects.filter(streamType=audiostreams)


    html = '<html><body>'


    html += str([(s.name, s.url_text) for s in audio])

    html += '</body></html>'

    return HttpResponse(html)


def AudioRecorder(request):
    if request.method == 'POST':
        form = MainFormAudio(request.POST)
        if form.is_valid():

            recorder = audio_recorder(name=form.cleaned_data['name'], url=form.cleaned_data['station'].url_text,
                                      time=form.cleaned_data['dauer'], partlength=form.cleaned_data['kapiteldauer'],
                                      timestamp=form.cleaned_data['timestamp'])
            n = recorder.getFilename()
            time = str(recorder.getTime())
            parts = recorder.getParts()

            threading.Thread(target=recorder.record, args=()).start()

            return render(request, 'recording.html', {'leng': time, 'name': n, 'parts': parts})

    else:
        a = (StreamType.objects.filter(id=2)[0])
        audio = Station.objects.filter(streamType=a)

        form = MainFormAudio()

    return render(request, 'Form.html', {'form': form})


def VideoRecorder(request):
    if request.method == 'POST':
        form = MainFormVideo(request.POST)
        if form.is_valid():

            recorder = video_recorder(name=form.cleaned_data['name'].replace(" ", "_"),
                                      recording_string=form.cleaned_data['station'].url_text,
                                      time=form.cleaned_data['dauer'], quiet=True,
                                      timestamp=form.cleaned_data['timestamp'])
            n = recorder.getFilename()
            time = str(recorder.getTime())
            threading.Thread(target=recorder.record, args=()).start()

            return render(request, 'recording.html', {'leng': time, 'name': n})

    else:
        form = MainFormVideo()

    return render(request, 'Form.html', {'form': form})


def addStations(request):
    if request.method == 'POST':
        form = newstationform(request.POST)

        if form.is_valid():
            s = StreamType.objects.get(stream_type=form.cleaned_data['typ'])
            s.station_set.create(name=form.cleaned_data['name'], url_text=form.cleaned_data['urlstring'],
                                 encoding=form.cleaned_data['kodierung'])
            print 'lala'
            s.save()

            return render(request, 'stations.html', {'name': form.cleaned_data['name']})
    else:

        form = newstationform()
    return render(request, 'Form.html', {'form': form})


def showFile(request, rfile):

    if not os.path.isfile(os.path.join(BASEDIR, 'static', rfile)):
        rfile = None

    return render(request, 'file.html', {'datei': rfile})


def showFiles(request, rfile, count=None):
    print '#COUNT#', count

    filelist = None
    if not os.path.isfile(os.path.join(BASEDIR, 'static', rfile)):
        if count:
            rfile_left = rfile[:-4]
            rfile_right = rfile[-4:]

            rfile = rfile_left + '_0' + rfile_right
            print '#RFILE#', rfile
            if os.path.isfile(os.path.join(BASEDIR, 'static', rfile)):
                try:
                    filelist = [str(rfile_left + '_' + str(r) + rfile_right) for r in range(int(count))]

                    a = list()
                    for g in filelist:

                        if os.path.isfile(os.path.join(BASEDIR, 'static', g)):
                            a.append(g)
                    filelist = a

                except ValueError:
                    print '#ERROR#'


        rfile = None




    return render(request, 'file.html', {'datei': rfile, 'count': count, 'filelist': filelist})


def showAudioFiles(request):
    filelist = []
    for files in os.listdir(os.path.join(BASEDIR, 'static')):
        if files.endswith("mp3") or files.endswith('.ogg') or files.endswith('wma'):
            filelist.append(files)
    return render(request, 'file.html', {'filelist': filelist})



def showVideoFiles(request):
    filelist = []
    for files in os.listdir(os.path.join(BASEDIR, 'static')):
        if files.endswith("mp4") or files.endswith('.flv') or files.endswith('wmv'):
            filelist.append(files)
    return render(request, 'file.html', {'filelist': filelist})


def showAudioFileListforTagging(request):
    filelist = []
    for files in os.listdir(os.path.join(BASEDIR, 'static')):
        if files.endswith("mp3") or files.endswith('.ogg') or files.endswith('wma'):
            filelist.append(files)
    return render(request, 'file.html', {'filelist': filelist, 'tag': True})

def tagger(request, tfile):
    mp3tag = mp3tagger(os.path.join(BASEDIR, 'static', tfile))
    t = mp3tag.getTitle()
    if t:
        t = t.split('\0')[0]
    k = mp3tag.getArtist()
    if k:
        k = k.split('\0')[0]
    alb = mp3tag.getAlbum()
    if alb:
        alb = alb.split('\0')[0]
    ja = mp3tag.getYear()
    if ja:
        ja = ja.split('\0')[0]
    h = mp3tag.getPublisher()
    if h:
        h = h.split('\0')[0]
    tn = mp3tag.getTrackNumber()
    if tn:
        tn = tn.split('\0')[0]
    message = ''

    if request.method == 'POST':
        form = taggform(request.POST)
        if form.is_valid():
            titel = form.cleaned_data['titel']
            album = form.cleaned_data['albums']
            kuenstler = form.cleaned_data['kuenstler']
            jahr = form.cleaned_data['jahr']
            herausgeber = form.cleaned_data['herausgeber']
            titelnummer = form.cleaned_data['titelnummer']

            retval = mp3tag.putTitle(titel) and mp3tag.putE1(kuenstler) and mp3tag.putAlbum(album)
            retval = retval and mp3tag.putYear(jahr) and mp3tag.putPublisher(herausgeber)
            retval = retval and mp3tag.putTrackNumber(titelnummer)
            mp3tag.mp3tag.commit()
            message = "Eintrag fehlgeschlagen"
            if retval:
                message = "Eintrag erfolgreich"


    else:
        form = taggform(initial={'albums': alb,
                                 'herausgeber': h,
                                 'jahr': ja,
                                 'kuenstler': k,
                                 'titel': t,
                                 'titelnummer': tn})
      #  form.albums.initial = alb
      #  form.herausgeber.initial = h
      #  form.jahr.initial = ja
      #  form.kuenstler.initial = k
      #  form.titel.initial = t
      #  form.titelnummer.initial = tn

    return render(request, 'tagger.html', {'message': message, 'form': form})
