from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from walks.models import Walk
from routes.models import Route

class TestIndexView(TestCase):

    def setUp(self):
        """Set up the test client and create test data."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.walk = Walk.objects.create(
            title='Test Walk',
            slug='test-walk',
            difficulty=None,
            elevation_gain=200,
            distance=10.5,
            featured_img='static/images/test.jpg',
            map_img='static/images/test_map.jpg',
            content='A beautiful walk along the coast.',
            featured=True,
            status=1
        )
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
        self.index_url = reverse('home')

    def test_index_view_get_authenticated(self):
        """Test the GET request to the index view for authenticated user.
        
        Verifies that the response status is 200, the correct template is used,
        and the context contains the correct data.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('walks', response.context)
        self.assertIn('routes', response.context)
        self.assertIn('total_distance', response.context)
        self.assertIn('total_elevation', response.context)
        self.assertIn('distance_left', response.context)
        self.assertIn('route_count', response.context)
        self.assertEqual(response.context['total_distance'], '10.50')
        self.assertEqual(response.context['total_elevation'], '200.00')
        self.assertEqual(response.context['distance_left'], '619.50')
        self.assertEqual(response.context['route_count'], 1)

    def test_index_view_get_unauthenticated(self):
        """Test the GET request to the index view for unauthenticated user.
        
        Verifies that the response status is 200, the correct template is used,
        and the context contains the correct data.
        """
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('walks', response.context)
        self.assertIn('routes', response.context)
        self.assertIn('total_distance', response.context)
        self.assertIn('total_elevation', response.context)
        self.assertIn('distance_left', response.context)
        self.assertIn('route_count', response.context)
        self.assertEqual(response.context['total_distance'], 0)
        self.assertEqual(response.context['total_elevation'], 0)
        self.assertEqual(response.context['distance_left'], 630)
        self.assertEqual(response.context['route_count'], 0)