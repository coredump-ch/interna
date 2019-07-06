from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from crowdfund import urls as crowdfund_urls
from front import urls as front_urls
from inventory import urls as inventory_urls
from memberdb import urls as memberdb_urls


def robots(r):
    return HttpResponse('User-agent: *\nDisallow: /', content_type='text/plain')


urlpatterns = [
    path('', include(front_urls)),
    path('', include(memberdb_urls)),
    path('crowdfund/', include(crowdfund_urls)),
    path('inventory/', include(inventory_urls)),
    path('admin/', admin.site.urls),
    path('robots.txt', robots)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
