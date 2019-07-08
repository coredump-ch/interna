from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('items/<str:pk>/', views.Detail.as_view(), name='detail'),
    path('items/<str:pk>/label/', views.Label.as_view(), name='label'),
]
