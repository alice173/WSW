from . import views
from django.urls import path
from .views import RouteList, RouteFormPage

urlpatterns = [
    path('', views.RouteList.as_view(), name='routes'),
    path('map/', RouteFormPage.as_view(), name='route_create'),
]