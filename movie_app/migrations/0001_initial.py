# Generated by Django 5.0.6 on 2024-07-01 23:40

import movie_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'db_table': 'addresses',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Casts',
                'db_table': 'casts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Genres',
                'db_table': 'genres',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Movies',
                'db_table': 'movies',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieCast',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Movie Casts',
                'db_table': 'movie_cast',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Movie Genres',
                'db_table': 'movie_genres',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieImage',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Movie Images',
                'db_table': 'movie_images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Profiles',
                'db_table': 'profiles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Reviews',
                'db_table': 'reviews',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
               
            ],
            options={
                'verbose_name_plural': 'User Images',
                'db_table': 'user_images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                
            ],
            options={
                'verbose_name_plural': 'Watch Lists',
                'db_table': 'watchlists',
                'managed': False,
            },
        ),
    ]
