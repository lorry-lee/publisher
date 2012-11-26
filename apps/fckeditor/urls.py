from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # (r'^fckeditor/editor/fckeditor_connector/uploader/$', 'publisher.apps.fckeditor.connector.views.uploader'),
    # (r'^fckeditor/editor/fckeditor_connector/browser/$', 'publisher.apps.fckeditor.connector.views.browser'),
    url(r'^fckeditor/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.FCKEDITOR_MEDIA_ROOT},name='get_fckeditor_media_files'),
)
