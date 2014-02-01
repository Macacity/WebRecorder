# -*- encoding: utf-8 -*-
from tagger import ID3v2

__author__ = 'LPC'


class mp3tagger(object):
    def __init__(self, musicfile):
        self.mp3tag = ID3v2(musicfile)


    ###put
    def putTitle(self, text):
        # TIT2 ['Emotional']
        frameid = "TIT2"
        return self.putFrame(text,  frameid)

    def putYear(self, text):
        #TYER ['1999']
        frameid = "TYER"
        return self.putFrame(text,  frameid)

    def putPublisher(self, text):
        #TPUB ['EMI']
        frameid = "TPUB"
        return self.putFrame(text,  frameid)

    def putAlbum(self, text):
        #TALB ['Final Curtain: The Ultimate Best of Falco']
        frameid = "TALB"
        return self.putFrame(text,  frameid)

    def putE2(self, text):
        #TPE2 ['Falco']
        frameid = "TPE2"
        return self.putFrame(text,  frameid)

    def putTrackNumber(self, text):
        #TRCK ['17']
        frameid = "TRCK"
        return self.putFrame(text,  frameid)

    def putComponist(self, text):
        #TCOM ['Falco/Ferdi Bolland/Rob Bolland']
        frameid = "TCOM"
        return self.putFrame(text,  frameid)

    def putE1(self, text):
        #TPE1 ['Falco']
        frameid = "TPE1"
        return self.putFrame(text,  frameid)

    def putFrame(self, text, frameid):
        new_frame = self.mp3tag.new_frame(frameid)
        new_frame.set_text(text)
        try:
            old_frame = [frame for frame in self.mp3tag.frames if frame.fid == frameid][0]
            self.mp3tag.frames.remove(old_frame)
        except IndexError:
            pass
        try:
            self.mp3tag.frames.append(new_frame)
            return True
        except Exception:
            return False

    def putFrames(self, fdict):
        retval = True
        for f in fdict:
            retval = retval and self.putFrame(fdict[f], f)
        self.mp3tag.commit()
        return retval

    ###GET
    def getTitle(self):
        # TIT2 ['Emotional']
        frameid = "TIT2"
        return self.getFrameText(frameid)

    def getYear(self):
        #TYER ['1999']
        frameid = "TYER"
        return self.getFrameText(frameid)

    def getPublisher(self):
        #TPUB ['EMI']
        frameid = "TPUB"
        return self.getFrameText(frameid)

    def getAlbum(self):
        #TALB ['Final Curtain: The Ultimate Best of Falco']
        frameid = "TALB"
        return self.getFrameText(frameid)

    def getE2(self):
        #TPE2 ['Falco']
        frameid = "TPE2"
        return self.getFrameText(frameid)

    def getTrackNumber(self):
        #TRCK ['17']
        frameid = "TRCK"
        return self.getFrameText(frameid)

    def getComponist(self):
        #TCOM ['Falco/Ferdi Bolland/Rob Bolland']
        frameid = "TCOM"
        return self.getFrameText(frameid)

    def getE1(self):
        #TPE1 ['Falco']
        frameid = "TPE1"
        return self.getFrameText(frameid)

    def getArtist(self):
        return self.getE1()

    def getFrameText(self, frameid):

        try:
            return [frame for frame in self.mp3tag.frames if frame.fid == frameid][0].strings[0]
        except IndexError:
            return None

    def getFrame(self, frameid):

        try:
            return [frame for frame in self.mp3tag.frames if frame.fid == frameid][0]
        except IndexError:
            return None

    def getFrames(self, flist):
        for f in flist:
            yield self.getFrame(f)


if __name__ == '__main__':

    a = "D:\\Daten\\Workspaces\\Python\\Python Programming\\ObjScript\\17-Emotional.mp3"
    b = mp3tagger(a)
    b.putE1("asd")