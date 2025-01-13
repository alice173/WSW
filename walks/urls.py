from . import views
from django.urls import path
from .views import WalkList


urlpatterns = [
    path('', views.WalkList.as_view(), name='walks'),
    path('<slug:slug>/', views.WalkDetail.as_view(), name='walk_detail'),
]