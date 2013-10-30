from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()

robots = lambda r: HttpResponse('User-agent: *\nDisallow: /', mimetype='text/plain')

urlpatterns = patterns('',
    url(r'^', include('front.urls')),
    url(r'^', include('memberdb.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', robots)
)
