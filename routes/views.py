import logging
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from .models import Route
from .forms import RouteForm

# Set up the logger
logger = logging.getLogger(__name__)

# List view for displaying routes
class RouteList(generic.ListView):
    queryset = Route.objects.all()
    template_name = 'routes/my-walks.html'
    context_object_name = 'routes'
    
    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'You must be registered to view this page.')
        return super().dispatch(request, *args, **kwargs)

# Detail view for displaying a single walk
class RouteDetail(generic.DetailView):
    model = Route
    template_name = 'routes/route_detail.html'
    context_object_name = 'route'

# View for route creation page
class RouteFormPage(generic.View):
    def get(self, request, *args, **kwargs):
        form = RouteForm()
        return render(
            request, 
            'routes/add-route.html', 
            {
                'form': form,
                'route': None  # Explicitly set route to None for create
            }
        )

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST, request.FILES)
        if form.is_valid():
            route = form.save(commit=False)
            route.user = request.user
            route.save()
            
            messages.success(
                request, 
                f'Route saved successfully! Visit <a href="{reverse("my_walks")}">My Walks</a> to see or edit your routes.'
            )
            return HttpResponseRedirect(reverse('route_create'))
        else:
            logger.warning('Form submission failed. Errors: %s', form.errors)
            return render(
                request, 
                'routes/route_create.html', 
                {
                    'form': form,
                    'route': None
                }
            )

# View for route edit page
def route_edit(request, route_id):
    """
    View to edit a route
    """
    route = get_object_or_404(Route, pk=route_id)


    if request.method == "POST":
        route_form = RouteForm(data=request.POST, instance=route)

        if route_form.is_valid() and route.user == request.user:
            route = route_form.save(commit=False)
            route.save()
            messages.add_message(request, messages.SUCCESS, 'Route updated successfully!')
            return HttpResponseRedirect(reverse('route_detail', args=[route_id]))
        else:
            messages.add_message(request, messages.ERROR, 'Error updating route!')

    else:
        route_form = RouteForm(instance=route)

    return render(request, 'routes/add-route.html', {
        'form': route_form, 
        'route': route, 
        
    })

# View for route deletion
def route_delete(request, route_id):
    """
    View to delete a route
    """
    route = get_object_or_404(Route, pk=route_id)

    if request.method == "POST":
        if route.user == request.user:
            route.delete()
            messages.add_message(request, messages.SUCCESS, 'Route deleted successfully!')
            return redirect('my_walks')
        else:
            messages.add_message(request, messages.ERROR, 'Error deleting route!')
            return redirect('my_walks')
    return redirect('my_walks')

# New view for displaying all routes on a map
def routes_map_view(request):
    """
    View to display all user's routes on a map
    """
    routes = Route.objects.filter(user=request.user)
    all_routes = []
    
    for route in routes:
        route_dict = {
            'id': route.id,
            'title': route.title,
            'start_point': route.start_point,
            'end_point': route.end_point,
            'distance': route.distance,
            'elevation': route.elevation,
            # Convert CloudinaryField to URL string
            'route_img': str(route.route_img.url) if route.route_img else None
        }
        all_routes.append(route_dict)
    
    return render(request, 'routes/routes_map.html', {
        'all_routes': all_routes
    })