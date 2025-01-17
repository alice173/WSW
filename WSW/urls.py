"""
URL configuration for WSW project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from routes.views import  RouteList, RouteFormPage, RouteDetail, route_edit, route_delete

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('walks/', include("walks.urls"), name="walks"),
    path('my-walks/', include("routes.urls"), name="my-walks"),
    path('map/', RouteFormPage.as_view(), name='route_create'),
    path('route/<int:pk>/', RouteDetail.as_view(), name='route_detail'),
    path('route/<int:route_id>/delete/', route_delete, name='route_delete'),
  
  
    
  
]
