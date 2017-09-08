from django.conf.urls import url

from . import views

app_name = 'crowdfund'

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^projects/new/$', views.Create.as_view(), name='create'),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.Detail.as_view(), name='detail'),
    url(r'^projects/(?P<pk>[0-9]+)/edit/$', views.Edit.as_view(), name='edit'),
]
