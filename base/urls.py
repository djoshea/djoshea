from django.conf.urls.defaults import *
from django.contrib import admin
from os.path import dirname, join

admin.autodiscover()

media_root = join(dirname(__file__), 'media')

urlpatterns = patterns('django.views.static',
    (r'^media/(?P<path>.*)$', 'serve', 
     {'document_root': media_root}),         
)

