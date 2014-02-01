from django.conf.urls import patterns, include, url
import Stations.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^stations/$', 'Stations.views.getStations'),
    url(r'^record/$', 'Stations.views.AudioRecorder'),
    url(r'^audio/$', 'Stations.views.AudioRecorder'),
    url(r'^aufnahme/([^/]*)/$', 'Stations.views.showFiles'),
    url(r'^aufnahme/([^/]*)/(\d+)/$', 'Stations.views.showFiles'),
    url(r'^audio/aufnahme/$', 'Stations.views.showAudioFiles'),
    url(r'^video/aufnahme/$', 'Stations.views.showVideoFiles'),
    url(r'^video/$', 'Stations.views.VideoRecorder'),
    url(r'^addstation/$', 'Stations.views.addStations'),
    url(r'^tagger/$', 'Stations.views.showAudioFileListforTagging'),
    url(r'^tagger/([^/]*)/$', 'Stations.views.tagger'),
    url(r'^$', 'Stations.views.AudioRecorder'),
    # url(r'^WebRecorder/', include('WebRecorder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
