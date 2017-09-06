from django.conf.urls import url

from . import views

app_name = 'crowdfund'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^projects/new/$', views.CreateView.as_view(), name='create'),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
