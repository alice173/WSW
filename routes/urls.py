from . import views
from django.urls import path
from .views import RouteList, RouteFormPage, RouteDetail, route_edit

urlpatterns = [
    path('', RouteList.as_view(), name='routes'),
    path('map/', RouteFormPage.as_view(), name='route_create'),
    path('my-walks/', RouteList.as_view(), name='my_walks'),
    path('route/<int:pk>/', RouteDetail.as_view(), name='route_detail'),
    path('route/<int:route_id>/edit/', route_edit, name='route_edit'), 
]