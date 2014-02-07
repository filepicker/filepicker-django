import re
import urllib
import os

from django.core.files import File


class FilepickerFile(File):
    filepicker_url_regex = re.compile(
            r'https?:\/\/www.filepicker.io\/api\/file\/.*')

    def __init__(self, url, additional_params={}):
        '''
        url should be a Filepicker URL pointing at a file reference.

        additional_params should include key/values such as:
        {
          'data-fp-signature': HEXDIGEST,
          'data-fp-policy': HEXDIGEST,
        }
        (it should look like additional_params of the models)
        '''
        if not self.filepicker_url_regex.match(url):
            raise ValueError('Not a filepicker.io URL: %s' % url)
        self.url = url
        self.set_additional_params(additional_params)
        # This helps Django File understand the File is not yet open.
        self.name = ""

    def set_additional_params(self, additional_params={}):
        '''
        Sets self.additional_params. Returns nothing.
        If called with no arguments, self.additional_parms will be cleared.
        '''
        self.additional_params = additional_params

    def get_url(self):
        '''
        Constructs the upstream Filepicker URL for reading/downloading on top
        of self.url passed into the constructor.
        '''
        if not self.additional_params:
            return self.url

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
        return url

    def get_file(self, reset=True):
        '''
        Downloads the file from filepicker.io and returns a
        Django File wrapper object.

        If a file has been downloaded with an explicit call to get_file, run
        cleanup to remove that file from the context. Otherwise get_file will
        return the current file.

        If get_file returns the current file as above, reset=True indicates that
        the descriptor pointer should be reset to the beginning of the file.
        reset=False indicates that the file pointer should be left as-is.
        '''
        if hasattr(self, 'file'):
            if not self.file.closed:
                # If there is a current file context, return self.
                if reset:
                    self.seek(0)
                return self
            else:
                # Closed file means we might as well cleanup and get_file()
                self.cleanup()

        # construct a URL for reading from Filepicker
        url = self.get_url()

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

        tempfile = open(self.filename, 'r')
        # initialize File components of this object
        super(FilepickerFile, self).__init__(tempfile,name=name)
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

        # This helps Django File understand the File is not yet open.
        self.name = ""

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
