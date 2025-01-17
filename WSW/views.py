from django.shortcuts import render
from walks.models import Walk
from routes.models import Route

def index(request):
    walks = Walk.objects.filter(featured=True)
    total_distance = Route.total_distance()
    total_elevation = Route.total_elevation()
    routes = Route.objects.all()
    context = {
        'walks': walks,
        'routes': routes,
    }
    return render(request, 'index.html', context)