from django.shortcuts import render
from django.views import generic
from .models import Route

# Create your views here.
class RouteList(generic.ListView):
    queryset = Route.objects.all
    template_name = 'routes/my-walks.html'
    context_object_name = 'routes'