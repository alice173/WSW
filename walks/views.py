from django.shortcuts import render
from django.views import generic
from .models import Walk


# Create your views here.
class WalkList(generic.ListView):
    queryset = Walk.objects.all
    template_name = 'walks/walks.html'
    context_object_name = 'walks'
