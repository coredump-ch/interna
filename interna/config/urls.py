from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse

from front import urls as front_urls
from memberdb import urls as memberdb_urls
from crowdfund import urls as crowdfund_urls


def robots(r):
    return HttpResponse('User-agent: *\nDisallow: /', mimetype='text/plain')


urlpatterns = [
    url(r'^', include(front_urls)),
    url(r'^', include(memberdb_urls)),
    url(r'^crowdfund/', include(crowdfund_urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^robots\.txt$', robots)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
