# Generated by Django 4.1.3 on 2022-11-24 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_bookings', '0003_cinemaseats_city_alter_movies_movie_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='total_seats',
            field=models.IntegerField(default=0),
        ),
    ]
