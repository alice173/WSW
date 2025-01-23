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

# view for add route page
class RouteFormPage(generic.View):
    def get(self, request, *args, **kwargs):
        form = RouteForm()
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
            
        return render(
            request, 
            'routes/map.html', 
            {
                'form': form, 
                'all_routes': all_routes,
                'route': None  # Explicitly set route to None for create
            }
        )

        def post(self, request, *args, **kwargs):
            form = RouteForm(request.POST, request.FILES)
            if form.is_valid():
                route = form.save(commit=False)
                route.user = request.user
                route.save()
                
                # Prepare response data
                response_data = {
                    'success': True,
                    'message': 'Route saved successfully!',
                    'redirect_url': reverse('my_walks')
                }
                
                messages.success(
                    request, 
                    f'Route saved successfully! Visit <a href="{reverse("my_walks")}">My Walks</a> to see or edit your routes.'
                )
                return HttpResponseRedirect(reverse('route_create'))
            else:
                logger.warning('Form submission failed. Errors: %s', form.errors)
                all_routes = Route.objects.filter(user=request.user).values(
                    'id', 'start_point', 'end_point', 'distance', 'elevation'
                )
                return render(
                    request, 
                    'routes/map.html', 
                    {
                        'form': form,
                        'all_routes': list(all_routes),
                        'route': None
                    }
            )

def route_edit(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    all_routes = list(Route.objects.filter(user=request.user).values())

        # Serialize route for template
    route_dict = {
        'id': route.id,
        'start_point': route.start_point,
        'end_point': route.end_point,
        'distance': route.distance,
        'elevation': route.elevation,
        'time_taken': route.time_taken,
        'route_img': str(route.route_img.url) if route.route_img else None
    }
    
    # Serialize all routes
    all_routes = []
    for route_obj in routes:
        route_dict = {
            'id': route_obj.id,
            'start_point': route_obj.start_point,
            'end_point': route_obj.end_point,
            'distance': route_obj.distance,
            'elevation': route_obj.elevation,
        }
        all_routes.append(route_dict)

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

    return render(
        request, 
        'routes/map.html', 
        {
            'form': route_form, 
            'route': route,
            'all_routes': all_routes  # Add all_routes to edit view context
        }
    )

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