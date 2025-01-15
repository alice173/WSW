from . import views
from django.urls import path
from .views import RouteList, RouteFormPage, RouteDetail

urlpatterns = [
    path('', views.RouteList.as_view(), name='routes'),
    path('map/', RouteFormPage.as_view(), name='route_create'),
    path('route/<int:pk>/', RouteDetail.as_view(), name='route_detail'),
]