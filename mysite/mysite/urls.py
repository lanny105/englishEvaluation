from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
                       # Examples:
                       url(r'^learn/index1.html$', 'learn.views.index', name='home'),# Notice this line
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^learn/index1.html#textbody', 'learn.views.index',name='home'),# Notice this line
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_URL})
                       )

