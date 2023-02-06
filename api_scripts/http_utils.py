import os
import urllib.request


def get_audio_file(url):
    filename = '../audio.ogg'
    urllib.request.urlretrieve(url, filename)
    return filename
