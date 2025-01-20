from . import views
from django.urls import path
from .views import RouteList, RouteFormPage, RouteDetail, route_edit, route_delete
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RouteList.as_view(), name='routes'),
    path('map/', RouteFormPage.as_view(), name='route_create'),
    path('my-walks/', RouteList.as_view(), name='my_walks'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('route/<int:pk>/', RouteDetail.as_view(), name='route_detail'),
    path('route/<int:route_id>/edit/', route_edit, name='route_edit'), 
    path('route/<int:route_id>/delete/', views.route_delete, name='route_delete'),
]