import json
from django.core.management.base import BaseCommand
from walks.models import Walk
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import walks from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to load data from')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r') as file:
            data = json.load(file)
            
            for walk in data['walks']:
                slug = slugify(walk['title'])
                unique_slug = slug
                num = 1
                while Walk.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{slug}-{num}"
                    num += 1
                
                Walk.objects.create(
                    title=walk['title'],
                    slug=unique_slug,
                    distance=walk['distance'],
                    elevation_gain=walk['elevation_gain'],
                    content=walk['content'],
                )
                self.stdout.write(f"Imported {walk['title']} with slug {unique_slug}")
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))