import logging
from django.shortcuts import render, redirect
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

# Detail view for displaying a single walk
class RouteDetail(generic.DetailView):
    model = Route
    template_name = 'routes/route_detail.html'
    context_object_name = 'route'

# Create view for handling the form
class RouteFormPage(generic.View):
    def get(self, request, *args, **kwargs):
        form = RouteForm()
        return render(request, 'routes/map.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST, request.FILES)
        if form.is_valid():
            route = form.save(commit=False)
            route.user = request.user  # Set the user
            route.save()
            return render(request, 'routes/map.html', {'form': RouteForm()})
        else:
            logger.warning('Form submission failed. Errors: %s', form.errors)
        return render(request, 'routes/map.html', {'form': form})
 