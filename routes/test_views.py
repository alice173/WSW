from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Route
from .forms import RouteForm

class TestRouteViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.route = Route.objects.create(
            title='Test Route',
            start_point='50.579749, -4.540113',
            end_point='50.694718, -3.954859',
            distance=10.5,
            elevation=200,
            date='2023-10-10',
            time_taken='2',
            comments='A beautiful walk along the coast.',
            user=self.user
        )
        self.route_create_url = reverse('route_create')
        self.route_edit_url = reverse('route_edit', args=[self.route.id])

    def test_route_create_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.route_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes/add-route.html')
        self.assertIsInstance(response.context['form'], RouteForm)

    def test_route_create_view_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.route_create_url, {
            'title': 'New Route',
            'start_point': '50.579749, -4.540113',
            'end_point': '50.694718, -3.954859',
            'distance': 12.5,
            'elevation': 250,
            'date': '2023-10-11',
            'time_taken': '3',
            'comments': 'Another beautiful walk along the coast.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Route.objects.filter(title='New Route').exists())

    def test_route_edit_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.route_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'routes/add-route.html')
        self.assertIsInstance(response.context['form'], RouteForm)
        self.assertEqual(response.context['form'].instance, self.route)

    def test_route_edit_view_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.route_edit_url, {
            'title': 'Updated Route',
            'start_point': '50.579749, -4.540113',
            'end_point': '50.694718, -3.954859',
            'distance': 15.5,
            'elevation': 300,
            'date': '2023-10-12',
            'time_taken': '4',
            'comments': 'Updated walk along the coast.'
        })
        self.assertEqual(response.status_code, 302)
        self.route.refresh_from_db()
        self.assertEqual(self.route.title, 'Updated Route')
        self.assertEqual(self.route.distance, 15.5)
        self.assertEqual(self.route.elevation, 300)