# Generated by Django 3.0.5 on 2022-02-27 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0017_auto_20220123_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='nodes_on_green_areas',
        ),
        migrations.RemoveField(
            model_name='route',
            name='nodes_on_non_green_areas',
        ),
    ]