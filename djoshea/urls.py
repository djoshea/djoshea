from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from base.settings import media_root_favicon

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'base/base.html'}),
    (r'^base/', include('base.urls')), 
)

urlpatterns += patterns('django.views.static',
    (r'^(?P<path>favicon\.(png|gif|ico))$', 'serve', 
      {'document_root': media_root_favicon }),

    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # (r'^admin/', include(admin.site.urls)),
)
