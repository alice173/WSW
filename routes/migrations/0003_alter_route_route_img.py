# Generated by Django 5.1.4 on 2025-01-15 13:15

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_route_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='route_img',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]