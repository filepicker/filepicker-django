import re
import urllib
from os.path import basename

from django.core.files import File


class FilepickerFile(object):
    filepicker_url_regex = re.compile(
            r'https?:\/\/www.filepicker.io\/api\/file\/.*')

    def __init__(self, url):
        if not self.filepicker_url_regex.match(url):
            raise ValueError('Not a filepicker.io URL: %s' % url)
        self.url = url

    def get_file(self):
        '''
        Downloads the file from filepicker.io and returns a
        Django File wrapper object
        '''
        filename, header = urllib.urlretrieve(self.url)
        name = basename(filename)
        disposition = header.get('Content-Disposition')
        if disposition:
            name = disposition.rpartition("filename=")[2].strip('" ')

        return File(open(filename, 'r'), name=name)
