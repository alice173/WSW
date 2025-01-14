from django.shortcuts import render, redirect
from django.views import generic
from .models import Route
from .forms import RouteForm

# List view for displaying routes
class RouteList(generic.ListView):
    queryset = Route.objects.all()
    template_name = 'routes/my-walks.html'
    context_object_name = 'routes'

# Create view for handling the form
class RouteFormPage(generic.View):
    def get(self, request, *args, **kwargs):
        form = RouteForm()
        return render(request, 'routes/map.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RouteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my_walks')  # Redirect to the route list view after saving
        return render(request, 'routes/map.html', {'form': form})