from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Walk


# Create your views here.
class WalkList(generic.ListView):
    queryset = Walk.objects.all
    template_name = 'walks/walks.html'
    context_object_name = 'walks'


class WalkDetail(generic.DetailView):
    model = Walk
    template_name = 'walks/walk_detail.html'
    context_object_name = 'walk'

    # def get_object(self):
    #     return get_object_or_404(Walk, pk=self.kwargs.get('pk'))
