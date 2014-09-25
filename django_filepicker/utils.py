import re
import os
import requests
import tempfile
from django.core.files import File


class FilepickerFile(File):
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

        if additional_params:
            for field in ('policy','signature'):
                longfield = 'data-fp-{0}'.format(field)
                if longfield in additional_params:
                    query_params[field] = additional_params[longfield]

        # Append the fields as GET query parameters to the URL in data.
        r = requests.get(self.url, params=query_params, stream=True)
        header = r.headers
        disposition = header.get('Content-Disposition')
        if disposition:
            name = disposition.rpartition("filename=")[2].strip('" ')
        filename = header.get('X-File-Name')
        if filename:
            name = filename

        # Create a temporary file to save to it later
        tmp = tempfile.NamedTemporaryFile(mode='w+b')
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                tmp.write(chunk) # Write the chunk
                tmp.flush()

        # initialize File components of this object
        super(FilepickerFile, self).__init__(tmp,name=name)
        return self

    def cleanup(self):
        '''
        Removes any downloaded objects and closes open files.
        '''
        # self.file comes from Django File
        if hasattr(self, 'file'):
            if not self.file.closed:
                self.file.close()
            delattr(self, 'file')

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
        self.get_file()
        # call Django's File context manager
        return super(FilepickerFile, self).__enter__()

    def __exit__(self, *args):
        # call Django's File context manager
        super(FilepickerFile, self).__exit__(*args)
        self.cleanup()

    def __del__(self):
        self.cleanup()
