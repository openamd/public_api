from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # TODO: remove trailing slashes
    (r'^locations/$', 'public_api_site.api.locations.index'),
    # NOTE: current testing
    (r'^testing/$',   'public_api_site.api.views.view'),

    (r'^speakers/$',  'public_api_site.api.views.speakers'),
    (r'^talks/$',     'public_api_site.api.talks.index'),
    (r'^interests/$', 'public_api_site.api.interests.index'),
    (r'^stats/$',     'public_api_site.api.stats.index'),


    # FIXME: we can probably ignore this
    (r'^speaker(?P<name>[^/]+)$', 'api.speakers.view'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
