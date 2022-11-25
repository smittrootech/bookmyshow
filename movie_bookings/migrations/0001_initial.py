# Generated by Django 4.1.3 on 2022-11-23 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CinemaHall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('total_seats', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('State', models.CharField(max_length=200)),
                ('zipcode', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('language', models.CharField(max_length=200)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('release_date', models.DateField()),
                ('country', models.CharField(max_length=200)),
                ('Genre', models.CharField(max_length=200)),
                ('movie_image_url', models.ImageField(blank=True, null=True, upload_to='movie/static/')),
                ('movie_image', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.ManyToManyField(blank=True, null=True, related_name='movies_in_city', to='movie_bookings.city')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('language', models.CharField(max_length=200)),
                ('cinema_hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='show_in_cinema', to='movie_bookings.cinemahall')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_name', to='movie_bookings.city')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movie_bookings.movies')),
            ],
        ),
        migrations.CreateModel(
            name='CinemaSeats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seatnumber', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver')], max_length=20)),
                ('cinema_hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cinema_hall', to='movie_bookings.cinemahall')),
                ('movie_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_movie', to='movie_bookings.movies')),
                ('show_time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_movie_show_time', to='movie_bookings.show')),
            ],
        ),
        migrations.AddField(
            model_name='cinemahall',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='movie_bookings.city'),
        ),
    ]
