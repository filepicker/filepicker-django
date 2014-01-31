import re
import urllib
import os

from django.core.files import File


class FilepickerFile(object):
    filepicker_url_regex = re.compile(
            r'https?:\/\/www.filepicker.io\/api\/file\/.*')

    def __init__(self, url):
        if not self.filepicker_url_regex.match(url):
            raise ValueError('Not a filepicker.io URL: %s' % url)
        self.url = url

    def get_file(self, additional_params={}):
        '''
        Downloads the file from filepicker.io and returns a
        Django File wrapper object.
        additional_params should include key/values such as:
        {
          'data-fp-signature': HEXDIGEST,
          'data-fp-policy': HEXDIGEST,
        }
        (in other words, parameters should look like additional_params
        of the models)
        '''
        # clean up any old downloads that are still hanging around
        self.cleanup()

        # Fetch any fields possibly required for fetching files for reading.
        query_params = {}
        for field in ('policy','signature'):
            longfield = 'data-fp-{0}'.format(field)
            if longfield in self.additional_params:
                query_params[field] = self.additional_params[longfield]
        # Append the fields as GET query parameters to the URL in data.
        query_params = urllib.urlencode(query_params)
        url = self.url
        if query_params:
            url = url + '?' + query_params

        # The temporary file will be created in a directory set by the
        # environment (TEMP_DIR, TEMP or TMP)
        self.filename, header = urllib.urlretrieve(url)
        name = os.path.basename(self.filename)
        disposition = header.get('Content-Disposition')
        if disposition:
            name = disposition.rpartition("filename=")[2].strip('" ')
        filename = header.get('X-File-Name')
        if filename:
            name = filename

        self.tempfile = open(self.filename, 'r')
        return File(self.tempfile, name=name)

    def cleanup(self):
        '''
        Removes any downloaded objects and closes open files.
        '''
        if hasattr(self, 'tempfile'):
            self.tempfile.close()
            delattr(self, 'tempfile')

        if hasattr(self, 'filename'):
            # the file might have been moved in the meantime so
            # check first
            if os.path.exists(self.filename):
                os.remove(self.filename)
            delattr(self, 'filename')

    def __enter__(self):
        '''
        Allow FilepickerFile to be used as a context manager as such:

            with FilepickerFile(url) as f:
                model.field.save(f.name, f.)
        '''
        return self.get_file()

    def __exit__(self, *args):
        self.cleanup()

    def __del__(self):
        self.cleanup()
