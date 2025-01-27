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
            'time_taken': '3',
            'comments': 'A beautiful walk along the coast.'
        })
        self.assertTrue(route_form.is_valid(), msg=route_form.errors)

    def test_title_is_required(self):
        """Test for the 'title' field"""
        route_form = RouteForm({
            'title': '',
            'start_point': '50.579749, -4.540113',
            'end_point': '50.694718, -3.954859',
            'distance': 10.5,
            'elevation': 200,
            'date': '2023-10-10',
            'time_taken': '3',
            'comments': 'A beautiful walk along the coast.'
        })
        self.assertFalse(route_form.is_valid(), msg="title is not provided")

    # test for the 'start_point' field  
    def test_start_point_is_required(self):
        """Test for the 'start_point' field"""
        route_form = RouteForm({
            'title': 'Nice walk',
            'start_point': '',
            'end_point': '50.694718, -3.954859',
            'distance': 10.5,
            'elevation': 200,
            'date': '2023-10-10',
            'time_taken': '3',
            'comments': 'A beautiful walk along the coast.'
        })
        self.assertFalse(route_form.is_valid(), msg="start point not provided")

    # test for the 'end_point' field
    def test_end_point_is_required(self):
        route_form = RouteForm({
            'title': 'Nice walk',
            'start_point': '50.579749, -4.540113',
            'end_point': '',
            'distance': 10.5,
            'elevation': 200,
            'date': '2023-10-10',
            'time_taken': '3',
            'comments': 'A beautiful walk along the coast.'
        })
        self.assertFalse(route_form.is_valid(), msg="end point not provided")

    # test for the 'distance' field
    def test_distance_is_required(self):
        route_form = RouteForm({
            'title': 'Nice walk',
            'start_point': '50.579749, -4.540113',
            'end_point': '50.694718, -3.954859',
            'distance': '',
            'elevation': 200,
            'date': '2023-10-10',
            'time_taken': '3',
            'comments': 'A beautiful walk along the coast.'
        })
        self.assertFalse(route_form.is_valid(), msg="distance not provided")

    # test for the 'elevation' field
    def test_elevation_is_required(self):
        route_form = RouteForm({
            'title': 'Nice walk',
            'start_point': '50.579749, -4.540113',
            'end_point': '50.694718, -3.954859',
            'distance': 10.5,
            'elevation': '',
            'date': '2023-10-10',
            'time_taken': '3',
            'comments': 'A beautiful walk along the coast.'
        })
        self.assertFalse(route_form.is_valid(), msg="elevation not provided")