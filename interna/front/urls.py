from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^auth/logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^members/$', views.MembersView.as_view(), name='members'),
)
