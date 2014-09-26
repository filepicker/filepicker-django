from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('filepicker_demo.urls', namespace='demo')),
    url(r'^admin/', include(admin.site.urls)),
)
