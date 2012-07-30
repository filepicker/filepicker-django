from django.forms import widgets
from django.core.files.base import File

import urllib2

INPUT_TYPE = 'filepicker-dragdrop'
DEFAULT_MIMETYPE = 'application/octet-stream'


class FPFileWidget(widgets.FileInput):
    input_type = INPUT_TYPE
    needs_multipart_form = False

    def value_from_datadict(self, data, files, name):
        #If we are using the middleware, then the data will already be
        #in FILES, if not it will be in POST
        if name not in data:
            return super(FPFileWidget, self).value_from_datadict(
                    data, files, name)

        url_fp = urllib2.urlopen(data[name])
        disposition = url_fp.info().getheader('Content-Disposition')
        if disposition:
            filename = disposition.rpartition("filename=")[2].strip('" ')
        else:
            filename = None

        file_obj = File(url_fp, filename)
        file_obj.size = long(url_fp.info().getheader('Content-Length', 0))
        file_obj.type = url_fp.info().getheader('Content-Type',
                DEFAULT_MIMETYPE)

        return file_obj
