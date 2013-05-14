from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # The demo page:
    url(r'^$', 'demo.filepicker_demo.views.home', name='home'),
)
