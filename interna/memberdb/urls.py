from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^api/members/active/$', views.ActiveMemberView.as_view(), name='api_members_active'),
)
