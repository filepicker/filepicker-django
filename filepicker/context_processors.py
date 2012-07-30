from django.utils.safestring import mark_safe


JS_VERSION = 0
JS_URL = "//api.filepicker.io/v%d/filepicker.js" % (JS_VERSION)


def js(request):
    return {"FILEPICKER_JS":
            mark_safe(u'<script src="%s"></script>' % JS_URL)}
