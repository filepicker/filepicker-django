from django.utils.safestring import mark_safe

#JS_URL is the url to the filepicker.io javascript library
JS_VERSION = 0
JS_URL = "//api.filepicker.io/v%d/filepicker.js" % (JS_VERSION)


def js(request):
    #Defines a {{FILEPICKER_JS}} tag that inserts the filepicker javascript library
    return {"FILEPICKER_JS":
            mark_safe(u'<script src="%s"></script>' % JS_URL)}
