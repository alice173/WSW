from django.shortcuts import render
from walks.models import Walk
from routes.models import Route

def index(request):
    walks = Walk.objects.filter(featured=True)
    total_distance = Route.total_distance()
    total_elevation = Route.total_elevation()
    route_count = Route.route_count()

    # Format to two decimal points
    total_distance = f"{total_distance:.2f}"
    total_elevation = f"{total_elevation:.2f}"
    distance_left = 630 - float(total_distance)
    distance_left = f"{distance_left:.2f}"

    routes = Route.objects.all()
    context = {
        'walks': walks,
        'routes': routes,
        'total_distance': total_distance,
        'total_elevation': total_elevation,
        'distance_left': distance_left,
        'route_count': route_count,
    }
    return render(request, 'index.html', context)