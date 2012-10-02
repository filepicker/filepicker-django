from django.utils.safestring import mark_safe
from .widgets import JS_URL

def js(request):
    #Defines a {{FILEPICKER_JS}} tag that inserts the filepicker javascript library
    return {"FILEPICKER_JS":
            mark_safe(u'<script src="%s"></script>' % JS_URL)}
