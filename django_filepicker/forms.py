from django import forms
from django.core.files import File
from django.conf import settings

from .widgets import FPFileWidget
import urllib2
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class FPFieldMixin():
    widget = FPFileWidget
    default_mimetypes = "*/*"

    def initialize(self, apikey=None, mimetypes=None, services=None):
        """
        Initializes the Filepicker field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        * services. Optional, the allowed services to pull from.
        """

        self.apikey = apikey or getattr(settings, 'FILEPICKER_API_KEY', None)
        if not self.apikey:
            raise Exception("Cannot find filepicker.io api key." +
            " Be sure to either pass as the apikey argument when creating the FPFileField," +
            " or set it as settings.FILEPICKER_API_KEY. To get a key, go to https://filepicker.io")

        self.mimetypes = mimetypes or self.default_mimetypes
        if not isinstance(self.mimetypes, basestring):
            #If mimetypes is an array, form a csv string
            try:
                self.mimetypes = ",".join(iter(self.mimetypes))
            except TypeError:
                self.mimetypes = str(self.mimetypes)

        self.services = services or getattr(settings, 'FILEPICKER_SERVICES', None)

    def widget_attrs(self, widget):
        attrs = {
                'data-fp-apikey': self.apikey,
                'data-fp-mimetypes': self.mimetypes,
                }

        if self.services:
            attrs['data-fp-option-services'] = self.services

        return attrs


class FPUrlField(FPFieldMixin, forms.URLField):
    widget = FPFileWidget
    default_mimetypes = "*/*"

    def __init__(self, *args, **kwargs):
        """
        Initializes the Filepicker url field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        * services. Optional, the allowed services to pull from.
        """
        self.initialize(
            apikey=kwargs.pop('apikey', None),
            mimetypes=kwargs.pop('mimetypes', None),
            services=kwargs.pop('services', None),
        )
        super(FPUrlField, self).__init__(*args, **kwargs)


class FPFileField(FPFieldMixin, forms.FileField):
    def __init__(self, *args, **kwargs):
        """
        Initializes the Filepicker url field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        * services. Optional, the allowed services to pull from.
        """
        self.initialize(
            apikey=kwargs.pop('apikey', None),
            mimetypes=kwargs.pop('mimetypes', None),
            services=kwargs.pop('services', None),
        )
        super(FPFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        """Takes the url in data and creates a File object"""
        if not data or not data.startswith('http'):
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
