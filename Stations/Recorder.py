__author__ = 'TJ'
# -*- coding: utf-8 -*-

import os
import subprocess

import time
import datetime
import requests


class audio_recorder:

    def __init__(self, url=None, name=None, time=None, partlength=None, timestamp=True):
        self._url = url
        self._timestamp = timestamp
        self._name = self._generateName(name)
        self._time = self.setTime(time)

        try:
            self._plength = datetime.timedelta(minutes=int(partlength))
        except TypeError:
            print 'PError: ', partlength
            self._plength = None

    def setTime(self, time):

        if not time:
            raise ValueError('No Time specified')

        t = time.split(":")

        if len(t) == 3:
            h, m, s = t

        elif len(t) == 2:
            h = 0
            m, s = t
        elif len(t) == 1:
            h = m = 0
            s, = t

        else:
            raise ValueError('No Time specified')

        if s < 3:
            raise ValueError('time range too small')

        return datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

    def getTime(self):
        return self._time.seconds

    def setName(self, name):
        self._name = self._generateName(name)

    def setUrl(self, url):
        self._url = url

    def _generateName(self, name):
        if not name or len(name) == 0:

            return str(datetime.datetime.now()).split('.')[0].replace(" ", "_").replace(":", "-")
        if not self._timestamp:

            return name

        return name + "_" + str(datetime.datetime.now()).split('.')[0].replace(" ", "_").replace(":", "-")

    def _setFilename(self, fn):
        BASEDIR = os.path.dirname(os.path.abspath(__file__))

        f = fn + ".mp3"
        return os.path.join(BASEDIR, 'static', f)

    def getName(self):
        return self._name

    def getFilename(self):
        return self._name + ".mp3"

    def getParts(self):
        if self._plength:
            parts = self._time.seconds / self._plength.seconds
            if self._time.seconds % self._plength.seconds:
                parts += 1
            return parts
        return 0

    def record(self):

        url = self._url
        r = requests.get(url, stream=True)
        self.size = 0
        name = self._name
        blocksize = 10

        if self._plength:
            until = time.mktime((datetime.datetime.now() + self._time).timetuple())-3

            parts = self._time.seconds / self._plength.seconds
            if self._time.seconds % self._plength.seconds:
                parts += 1

            f = []
            for i in range(parts):
                fo = open(self._setFilename(name+"_"+str(i)), "wb")
                f.append(fo)
            i = 0
            while time.time() < until:

                if i == 0:
                    part = time.mktime((datetime.datetime.now() + self._plength).timetuple())-3
                else:
                    part = time.mktime((datetime.datetime.now() + self._plength).timetuple())


                while time.time() < part and time.time() < until:
                   # print'#i:', i
                    block = r.raw.read(blocksize)
                    self.size += len(block)
                    if len(block) == 0:
                        break
                    #print time.time(), part, until
                    f[i].write(block)
                f[i].close()
                i += 1

        else:

            fo = open(self._setFilename(name), "wb")
            until = time.mktime((datetime.datetime.now() + self._time).timetuple())-3

            while time.time() < until:
                block = r.raw.read(blocksize)
                self.size += len(block)
                if len(block) == 0:
                    break
                fo.write(block)
                #

            fo.close()


class video_recorder(object):

    def __init__(self, name, recording_string, time, encoding="flv", quiet=False, timestamp=True):

        self._quiet = quiet
        self._url = recording_string

        self._time = self.setTime(time)
        self._encoding = encoding
        self.timestamp = timestamp
        self._name = self._generateName(name)

    def setTime(self, time):
        if not time:
            raise ValueError('No Time specified')
        t = time.split(":")
        if len(t) == 3:
            h, m, s = t
        elif len(t) == 2:
            h = 0
            m, s = t
        elif len(t) == 1:
            h = m = 0
            s, = t
        else:
            raise ValueError('No Time specified')

        return str(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).seconds)

    def getTime(self):
        return self._time

    def getFilename(self):
        return self._name + '.' + self._encoding

    def _generateName(self, name):
        if not name or len(name) == 0:
            return str(datetime.datetime.now()).split('.')[0].replace(" ", "_").replace(":", "-")
        if not self.timestamp:
            return name
        return name + "_" + str(datetime.datetime.now()).split('.')[0].replace(" ", "_").replace(":", "-")

    def _setFilename(self, fn):
        fn = fn + "." + self._encoding
        BASEDIR = os.path.dirname(os.path.abspath(__file__))
        #return '"' + fn + "." + self._encoding + '"'
        return os.path.join(BASEDIR, 'static', fn)

    def _generateCall(self, quiet=True):

        call = 'rtmpdump {} -o {} --live -B{}'\
            .format(self._url, self._setFilename(self._name), self._time)

        if quiet:
            call += ' -q'
        #print call
        return call

    def record(self):
        # Check for rtmpdump first
        try:
            subprocess.call(['rtmpdump', '-h'], stdout=(open(os.path.devnull, 'w')),
                            stderr=subprocess.STDOUT)
        except (OSError, IOError) as eoi:
            print (u'"rtmpdump" could not be run')
            print eoi
            return False
        if self._quiet:
            rtcode = subprocess.call(self._generateCall())
        else:
            rtcode = subprocess.call(self._generateCall(False))
        return rtcode

if __name__ == '__main__':
    print time.time()
    print time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=5)).timetuple())
    print str(datetime.datetime.now()).split('.')[0].replace(" ", "_")+".mp3"
    #a=recorder("http://gffstream.ic.llnwd.net/stream/gffstream_w11b", "RBB", seconds=30)
    #a=recorder("rtsp://daserste.edges.wowza.gl-systemhaus.de/live/daserste_de_1600", "RBB", time="5:00")

    a = video_recorder('Arte', '-r "rtmp://artestras.fc.llnwd.net/artestras" -a "artestras" '
                               '-f "LNX 11,0,1,98" -W "http://www.arte.tv/flash/mediaplayer/mediaplayer.swf"'
                               ' -p "http://videos.arte.tv/de/videos/html/index-4268756.html" '
                               '-y "s_artestras_scst_geoFRDE_de?s=1320220800&h=878865258ebb8eaa437b99c3c7598998"',
                       '00:0:10', encoding='flv', quiet=False)
    a.record()
