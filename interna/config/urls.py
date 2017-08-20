from django.conf.urls import include, url

from django.contrib import admin
from django.http import HttpResponse

from front import urls as front_urls
from memberdb import urls as memberdb_urls


def robots(r):
    return HttpResponse('User-agent: *\nDisallow: /', mimetype='text/plain')


urlpatterns = [
    url(r'^', include(front_urls)),
    url(r'^', include(memberdb_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^robots\.txt$', robots)
]
