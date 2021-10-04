from django.urls import path
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView

from . import views

app_name = 'front'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('auth/login/', LoginView.as_view(template_name='front/login.html'), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('members/', views.MembersView.as_view(), name='members'),
    path('members/emails/', views.MemberEmailsView.as_view(), name='member_emails'),
    path('wishlist/', TemplateView.as_view(template_name='front/wishlist.html'), name='wishlist'),
]
