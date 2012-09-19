from django import forms
from django.core.files import File
from django.conf import settings

import widgets
import urllib2
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class FPFileField(forms.FileField):
    widget = widgets.FPFileWidget
    default_mimetypes = "*/*"

    def __init__(self, *args, **kwargs):
        """
        Initializes the Filepicker file field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        """

        if 'apikey' in kwargs:
            self.apikey = kwargs.pop('apikey')
        elif hasattr(settings, 'FILEPICKER_API_KEY'):
            self.apikey = settings.FILEPICKER_API_KEY
        else:
            raise Exception("Cannot find filepicker.io api key." +
            " Be sure to either pass as the apikey argument when creating the FPFileField," +
            " or set it as settings.FILEPICKER_API_KEY. To get a key, go to https://filepicker.io")

        self.mimetypes = kwargs.pop('mimetypes', self.default_mimetypes)
        if not isinstance(self.mimetypes, basestring):
            #If mimetypes is an array, form a csv string
            try:
                self.mimetypes = ",".join(iter(self.mimetypes))
            except TypeError:
                self.mimetypes = str(self.mimetypes)

        super(FPFileField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = {
                'data-fp-apikey': self.apikey,
                'data-fp-mimetypes': self.mimetypes,
                }

        return attrs

    def to_python(self, data):
        """Takes the url in data and creates a File object"""
        if not data:
            return None

        url_fp = urllib2.urlopen(data)

        disposition = url_fp.info().getheader('Content-Disposition')
        if disposition:
            name = disposition.rpartition("filename=")[2].strip('" ')
        else:
            name = "fp-file"
        size = long(url_fp.info().getheader('Content-Length', 0))

        fp = File(StringIO(url_fp.read()), name=name)
        fp.size = size

        return fp
