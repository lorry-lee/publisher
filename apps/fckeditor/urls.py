from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # (r'^fckeditor/editor/fckeditor_connector/uploader/$', 'publisher.apps.fckeditor.connector.views.uploader'),
    # (r'^fckeditor/editor/fckeditor_connector/browser/$', 'publisher.apps.fckeditor.connector.views.browser'),
    (r'^fckeditor/editor/gallery/browse/$', 'publisher.apps.post.views.browsegallery'),
    (r'^fckeditor/editor/gallery/browse/(?P<page_id>\d+)/page/$', 'publisher.apps.post.views.browsegallery'),
    (r'^fckeditor/editor/gallery/upload/$', 'publisher.apps.post.views.uploadtogallery'),
    url(r'^fckeditor/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.FCKEDITOR_MEDIA_ROOT},name='get_fckeditor_media_files'),
)
