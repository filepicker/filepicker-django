from .utils import FilepickerFile


class URLFileMapperMiddleware(object):
    """
    This middleware will take any Filepicker.io urls that are posted to the server via a POST
    and put a matching File object into request.FILES. This way, if you're used to grabbing files out of
    request.FILES, you don't have to change your backend code when using the filepicker.io widgets.

    This middleware is rather agressive in that it will automatically fetch any and all filepicker
    urls passed to the server, so if you are already processing the files via FPFileField or similar
    this functionality is redundant

    Note that the original filepicker.io url will still be available in POST if you need it.
    """
    def process_request(self, request):
        #Iterate over GET or POST data, search for filepicker.io urls
        for key, val in request.POST.items():
            try:
                fp = FilepickerFile(val)
            except ValueError:
                pass
            else:
                splits = val.split(",")
                for url in splits:
                    if key in request.FILES:
                        request.FILES.setlist(key, list(
                            request.FILES.getlist(key) + [fp.get_file()]))
                    else:
                        request.FILES[key] = fp.get_file()
