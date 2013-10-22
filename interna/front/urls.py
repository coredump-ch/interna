from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^auth/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'front/login.html'}, name='login'),
    url(r'^auth/logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^members/$', views.MembersView.as_view(), name='members'),
    url(r'^coupons/$', views.CouponsView.as_view(), name='coupons'),
)
