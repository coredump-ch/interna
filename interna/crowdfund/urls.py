from django.urls import path

from . import views

app_name = 'crowdfund'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('projects/new/', views.Create.as_view(), name='create'),
    path('projects/<int:pk>/', views.Detail.as_view(), name='detail'),
    path('projects/<int:pk>/edit/', views.Edit.as_view(), name='edit'),
]
