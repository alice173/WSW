# Generated by Django 5.1.4 on 2025-01-10 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walks', '0002_walk_elevation_gain_difficultylevel_walk_difficulty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='difficultylevel',
            name='walk',
        ),
    ]