from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,BaseUserManager 
import random,uuid


def to_kebab_case(input_string):
    return input_string.replace(" ", "-").lower()


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True,null=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
    class Meta:
        managed = True
        db_table = "Users"
        verbose_name = "User"
        verbose_name_plural = "User"

class UserImage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(
        upload_to="images/user_images/", default="images/default/default_avatar.png"
    )
    is_main_image = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not UserImage.objects.filter(user=self.user).exists():
            self.is_main_image = True
        else:
            if self.is_main_image:
                UserImage.objects.filter(user=self.user).exclude(pk=self.pk).update(is_main_image=False)
        super().save(*args, **kwargs)
    class Meta:
        managed = True
        db_table = "UserImages"
        verbose_name = "User Image"
        verbose_name_plural = "User Images"

class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        db_table = "Countries"
        verbose_name = "Country"
        verbose_name_plural = "Countries"
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        db_table = "Genres"
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

class Actor(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        db_table = "Actors"
        verbose_name = "Actor"
        verbose_name_plural = "Actors"

class Director(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        db_table = "Directors"
        verbose_name = "Director"
        verbose_name_plural = "Directors"

class Movie(models.Model):
    TYPE = (('pg13','PG-13'),('r','R'),('g','G'))
    title = models.CharField(max_length=255)
    end_point = models.CharField(max_length=300, unique=True, default="", blank=True)
    description = models.TextField()
    release_date = models.DateField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    duration = models.PositiveIntegerField()
    rating = models.FloatField(default=0.0)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="movies")
    type = models.CharField(choices=TYPE,default='g',max_length=10)
    movie_file = models.FileField(upload_to='movies/')

    def __str__(self):
        return self.title
    
    def generate_unique_endpoint(self):
        return f"{to_kebab_case(self.title)}-{uuid.uuid4()}"
    def save(self, *args, **kwargs):
        if not self.end_point:
            self.end_point = self.generate_unique_endpoint()
        super(Movie, self).save(*args, **kwargs)
    class Meta:
        managed = True
        db_table = "Movies"
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genres')
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movie_genres')
    class Meta:
        managed = True
        db_table = "MovieGenres"
        verbose_name = "Movie Genre"
        verbose_name_plural = "Movie Genres"

class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_actors')
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='movie_actors')
    class Meta:
        managed = True
        db_table = "MovieActors"
        verbose_name = "Movie Actor"
        verbose_name_plural = "Movie Actors"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()  # Rating out of 10
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating})"
    
    class Meta:
        managed = True
        db_table = "Reviews"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='in_watchlists')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
    class Meta:
        managed = True
        db_table = "Watchlists"
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"

class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/movie_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_main_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not MovieImage.objects.filter(movie=self.movie).exists():
            self.is_main_image = True
        else:
            if self.is_main_image:
                MovieImage.objects.filter(movie=self.movie).exclude(pk=self.pk).update(is_main_image=False)
        super().save(*args, **kwargs)
    class Meta:
        managed = True
        db_table = "MovieImages"
        verbose_name = "Movie Image"
        verbose_name_plural = "Movie Images"
