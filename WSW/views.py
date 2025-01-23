from django.shortcuts import render
from walks.models import Walk
from routes.models import Route

def index(request):
    walks = Walk.objects.filter(featured=True)
    total_distance = 0
    total_elevation = 0
    route_count = 0
    distance_left = 630

    if request.user.is_authenticated:
        total_distance = Route.total_distance(request.user)
        total_elevation = Route.total_elevation(request.user)
        route_count = Route.route_count(request.user)

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