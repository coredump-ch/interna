from django.urls import path

from . import views

app_name = 'memberdb'

urlpatterns = [
    path('api/members/active/', views.ActiveMemberView.as_view(), name='api_members_active'),
]
