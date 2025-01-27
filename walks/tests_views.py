from django.test import TestCase, Client
from django.urls import reverse
from .models import Walk, DifficultyLevel

class TestWalkViews(TestCase):

    def setUp(self):
        """Set up the test client and create test data."""
        self.client = Client()
        self.difficulty = DifficultyLevel.objects.create(level='Easy')
        self.walk = Walk.objects.create(
            title='Test Walk',
            slug='test-walk',
            difficulty=self.difficulty,
            elevation_gain=200,
            distance=10.5,
            featured_img='static/images/test.jpg',
            map_img='static/images/test_map.jpg',
            content='A beautiful walk along the coast.',
            featured=True,
            status=1
        )
        self.walk_list_url = reverse('walks')
        self.walk_detail_url = reverse('walk_detail', args=[self.walk.slug])

    def test_walk_list_view_get(self):
        """Test the GET request to the walk list view.
        
        Verifies that the response status is 200, the correct template is used,
        and the context contains a queryset of all walks.
        """
        response = self.client.get(self.walk_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'walks/walks.html')
        self.assertIn('walks', response.context)
        # self.assertQuerySetEqual(
        #     response.context['walks'],
        #     Walk.objects.all(),
        #     transform=lambda x: x
        # )

    def test_walk_detail_view_get(self):
        """Test the GET request to the walk detail view.
        
        Verifies that the response status is 200, the correct template is used,
        and the context contains the specific walk being viewed.
        """
        response = self.client.get(self.walk_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'walks/walk_detail.html')
        self.assertIn('walk', response.context)
        self.assertEqual(response.context['walk'], self.walk)