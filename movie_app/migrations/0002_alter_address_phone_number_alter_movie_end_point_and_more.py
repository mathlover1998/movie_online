# Generated by Django 5.0.6 on 2024-07-07 07:19

import movie_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_number',
            field=movie_app.models.PhoneNumberValidators(max_length=15, validators=[movie_app.models.PhoneNumberValidators.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='movie',
            name='end_point',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=movie_app.models.PhoneNumberValidators(blank=True, max_length=15, validators=[movie_app.models.PhoneNumberValidators.validate_phone_number]),
        ),
    ]
