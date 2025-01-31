# Generated by Django 5.1.3 on 2025-01-31 07:46

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyimage',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=85, scale=None, size=[600, 600], upload_to='property_images/'),
        ),
    ]
