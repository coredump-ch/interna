from django.conf.urls import url

from . import views

app_name = 'memberdb'

urlpatterns = [
    url(r'^api/members/active/$', views.ActiveMemberView.as_view(), name='api_members_active'),
]
