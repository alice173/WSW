from . import views
from django.urls import path
urlpatterns = [
    path('', views.RouteList.as_view(), name='routes'),
    path('/map/', RouteFormPage.as_view(), name='route_create'),
]