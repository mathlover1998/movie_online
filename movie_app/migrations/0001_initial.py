# Generated by Django 5.0.6 on 2024-07-07 05:50

import django.db.models.deletion
import django.utils.timezone
import movie_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('role', models.CharField(choices=[('actor', 'Actor'), ('director', 'Director')], default='actor')),
                ('ranking', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Casts',
                'db_table': 'casts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('drama', 'Drama'), ('action', 'Action'), ('adventure', 'Adventure'), ('animation', 'Animation'), ('biography', 'Biography'), ('comedy', 'Comedy'), ('crime', 'Crime'), ('documentary', 'Documentary'), ('drama', 'Drama'), ('family', 'Family'), ('fantasy', 'Fantasy'), ('film_noir', 'Film Noir'), ('history', 'History'), ('horror', 'Horror'), ('music', 'Music'), ('musical', 'Musical'), ('mystery', 'Mystery'), ('romance', 'Romance'), ('sci_fi', 'Sci-Fi'), ('sport', 'Sport'), ('superhero', 'Superhero'), ('thriller', 'Thriller'), ('war', 'War'), ('western', 'Western')], default='drama')),
            ],
            options={
                'verbose_name_plural': 'Genres',
                'db_table': 'genres',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.DateField(default='1980-01-01')),
                ('end_point', models.CharField(default='', max_length=300)),
                ('runtime', models.IntegerField(default=0)),
                ('movie_url', models.FileField(upload_to='documents/')),
                ('synopsis', models.TextField(blank=True, null=True)),
                ('mpaa_rating', models.CharField(choices=[('g', 'G'), ('pg', 'PG'), ('pg-13', 'PG-13'), ('r', 'R')], default='g')),
                ('score', models.DecimalField(decimal_places=1, max_digits=3)),
                ('imdb_score', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
            options={
                'verbose_name_plural': 'Movies',
                'db_table': 'movies',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', movie_app.models.PhoneNumberValidators(max_length=15, validators=[movie_app.models.PhoneNumberValidators.validate_phone_number])),
                ('detail', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=20)),
                ('district', models.CharField(max_length=20)),
                ('commune', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'db_table': 'addresses',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MovieCast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_app.cast')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_app.movie')),
            ],
            options={
                'verbose_name_plural': 'Movie Casts',
                'db_table': 'movie_cast',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MovieImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(upload_to='images/movie_images/')),
                ('type', models.CharField(choices=[('poster', 'Poster'), ('backdrop', 'Backdrop'), ('screenshot', 'Screenshot')], default='backdrop')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='movie_app.movie')),
            ],
            options={
                'verbose_name_plural': 'Movie Images',
                'db_table': 'movie_images',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', movie_app.models.PhoneNumberValidators(blank=True, max_length=15, validators=[movie_app.models.PhoneNumberValidators.validate_phone_number])),
                ('info', models.TextField(blank=True)),
                ('first_name', models.CharField(default='', max_length=255)),
                ('last_name', models.CharField(default='', max_length=255)),
                ('display_name', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profiles',
                'db_table': 'profiles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('review_text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movie_app.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
                'db_table': 'reviews',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(blank=True, max_length=255, null=True)),
                ('image_url', models.ImageField(upload_to='images/user_images/')),
                ('is_primary', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Images',
                'db_table': 'user_images',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to='movie_app.movie')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Watch Lists',
                'db_table': 'watchlists',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_app.genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_app.movie')),
            ],
            options={
                'verbose_name_plural': 'Movie Genres',
                'db_table': 'movie_genres',
                'managed': True,
                'unique_together': {('movie', 'genres')},
            },
        ),
    ]
