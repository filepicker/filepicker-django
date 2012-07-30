from django.db import models
from django.core.files import File
from django.utils.translation import ugettext_lazy

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import urllib2

import forms


class FPFile(File):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing filepicker files
    """
    def __init__(self, file, name=None, url=None):
        super(FPFile, self).__init__(file, name=name)
        self.url = url
        print self.url

    def __eq__(self, other):
        return self.url == getattr(other, 'url', None)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.url)

    def _require_file(self):
        if not self.url and not self.file:
            raise ValueError("Cannot read input for Filepicker file - be sure to pass in a url")

    def _get_file(self):
        self._require_file(self)
        if not hasattr(self, '_url_file') or self._url_file is None:
            self._url_file = urllib2.open(self.url)
            name, size = self._get_info()
            self.name = name
            self.size = size
            #url files make everything annoying
            self._file = StringIO(self._url_file.read())
        return self._file

    def _set_file(self, file):
        del self.file
        self._file = file
        name, size = self._get_info()
        self.name = name
        self.size = size

    def _del_file(self):
        close = False
        if hasattr(self, '_url_file'):
            close = True
            del self._url_file
        if hasattr(self, '_file'):
            close = True
            del self._url_file

        if close:
            self.close()

    property(_get_file, _set_file, _del_file)

    def _get_info(self):
        self._require_file()
        if self.name:
            name = self.name
        else:
            disposition = self._url_file.info().getheader('Content-Disposition')
            if disposition:
                name = disposition.rpartition("filename=")[2].strip('" ')

        if self.size is not None:
            size = self.size
        else:
            size = long(self._url_file.info().getheader('Content-Length', 0))

        return name, size

    def open(self, mode='rb'):
        #will auto-open
        self._require_file()

    def seek(self, offset, whence=0):
        self._file.seek(offset, whence)

    def close(self):
        file = getattr(self, '_file', None)
        if file is not None:
            file.close()

        url_file = getattr(self, '_url_file', None)
        if url_file is not None:
            url_file.close()


class FPFileField(models.FileField):
    description = ugettext_lazy("A File selected using Filepicker.io")

    def formfield(self, **kwargs):
        print 'there', kwargs
        defaults = {'form_class': forms.FPFileField,
                'max_length': self.max_length}

        if 'initial' in kwargs:
            defaults['required'] = False

        defaults.update(kwargs)
        return super(FPFileField, self).formfield(**defaults)
