from django.test import TestCase
from .forms import RouteForm

class TestRouteForm(TestCase):

    def test_form_is_valid(self):
        route_form = RouteForm({
            'title': 'Nice walk',
            'start_point': '50.579749, -4.540113',
            'end_point': '50.694718, -3.954859',
            'distance': 10.5,
            'elevation': 200,
            'date': '2023-10-10',
            'time_taken': '2',
            'comments': 'A beautiful walk along the coast.'
        })
        self.assertTrue(route_form.is_valid(), msg=route_form.errors)