from . import views
from django.urls import path


urlpatterns = [
    path('', views.WalkList.as_view(), name='walks'),
]