from django import forms
from django.core.files import File
from django.conf import settings

import widgets
import urllib2

#Expects FILEPICKER_API_KEY to be set in settings


class FPFileField(forms.FileField):
    widget = widgets.FPFileWidget
    default_mimetypes = "*/*"

    def __init__(self, *args, **kwargs):
        self.apikey = kwargs.pop('apikey', settings.FILEPICKER_API_KEY)
        self.multiple = kwargs.pop('multiple', False)
        self.persist = kwargs.pop('persist', False)

        self.mimetypes = kwargs.pop('mimetypes', self.default_mimetypes)
        if not isinstance(self.mimetypes, basestring):
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

        if self.multiple:
            attrs['data-fp-multiple'] = "true"
        if self.persist:
            attrs['data-fp-persist'] = "true"

        return attrs

    def to_python(self, data):
        if not data:
            return None

        url_fp = urllib2.urlopen(data)

        disposition = url_fp.info().getheader('Content-Disposition')
        if disposition:
            name = disposition.rpartition("filename=")[2].strip('" ')
        else:
            name = "fp-file"
        size = long(url_fp.info().getheader('Content-Length', 0))

        fp = File(url_fp, name=name)
        fp.size = size

        return fp
