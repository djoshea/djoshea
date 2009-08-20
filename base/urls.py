from django.conf.urls.defaults import *
from django.contrib import admin
from settings import media_root

admin.autodiscover()

urlpatterns = patterns('django.views.static',
    (r'^media/(?P<path>.*)$', 'serve', 
     {'document_root': media_root}),         
)

