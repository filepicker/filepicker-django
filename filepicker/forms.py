from django import forms
from django.conf import settings

import widgets
import models

#Expects FILEPICKER_API_KEY to be set in settings


class FPFileField(forms.FileField):
    widget = widgets.FPFileWidget
    default_mimetypes = "*/*"

    def __init__(self, *args, **kwargs):
        print args, kwargs
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

        fp = models.FPFile(None, name=None, url=data)
        return fp
