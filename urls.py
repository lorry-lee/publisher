from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # post urls
    #(r'^YOUR_INSTANCE_NAME/',include('post.urls')),
    (r'^$', 'publisher.apps.post.views.index'),
    (r'^publisher', 'publisher.apps.post.views.index'),
    (r'^index', 'publisher.apps.post.views.index'),
    (r'^photologue/photos/(?P<path>.*)$','publisher.apps.post.views.test', {'document_root':settings.STATIC_ROOT + '/photologue/photos/'}),
    (r'^admin/(.*)', admin.site.root),
    (r'^photologue/', include('photologue.urls')),
    (r'^post/', include('publisher.apps.post.urls')),
    (r'^auth/', include('publisher.apps.auth.urls')),
    (r'^fckeditor/', include('publisher.apps.fckeditor.urls')),

    # static urls
    (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    (r'^pic/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT + '/pic/'}),
    (r'^scripts/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT + '/scripts/'}),
)

handler404 = 'apps.post.views.handler404'
handler500 = 'apps.post.views.handler500'
