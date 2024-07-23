from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser,BaseUserManager 
import random,uuid
from django.templatetags.static import static
from django.core.exceptions import ValidationError
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            
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
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True,null=True)
    objects = UserManager()


    USERNAME_FIELD = "email"

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
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserImage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='images')
    image_name = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.ImageField(upload_to="images/user_images/")
    is_primary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.profile.display_name
    
    @property
    def avatar(self):
        if self.image_url:
            return self.image_url.url
        return static("images/default/default_avatar.png")

    class Meta:
        managed = True
        db_table = 'user_images'
        verbose_name_plural = "User Images"

class PhoneNumberValidators(models.CharField):
    def __init__(self, *args, **kwargs) :
        kwargs['max_length'] = 15
        kwargs['validators'] = [self.validate_phone_number]
        super(PhoneNumberValidators,self).__init__(*args,**kwargs)

    def validate_phone_number(self,value):
        if not value.isdigit() and not value.startswith('+'):
            raise ValidationError('Phone number must only contain digits and optional + sign')

def extract_username(email):
    # Find the position of '@' symbol
    at_index = email.find('@')
    
    # Extract the substring before '@'
    if at_index != -1:
        username = email[:at_index]
    else:
        # Handle case where '@' is not found (though normally in email it should be present)
        username = email  # Entire email address is returned
    
    return username

def generate_short_uuid():
    # Generate a UUID
    generated_uuid = uuid.uuid4()

    # Convert UUID to a hexadecimal string without dashes
    uuid_hex = generated_uuid.hex

    # Take the first 6 characters from the hex string
    short_uuid = uuid_hex[:6]

    return short_uuid


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE,related_name='profile')
    phone_number = PhoneNumberValidators(blank=True)
    info = models.TextField(blank=True)
    first_name = models.CharField(max_length=255,null=False,default='')
    last_name = models.CharField(max_length=255,null=False,default='')
    display_name = models.CharField(max_length=255,null=False,blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def generate_display_name(self):
        return extract_username(self.user.email) + generate_short_uuid()
    
    def save(self,*args, **kwargs):
        if not self.display_name:
            self.display_name = self.generate_display_name()
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'profiles'
        verbose_name_plural = "Profiles"

class Address(models.Model):
    ADDRESS_TYPE = (('home','Home'),('office','Office'),('other','Other'))
    user = models.ForeignKey(User, models.CASCADE,related_name='addresses')
    name = models.CharField(max_length=100,null=False)
    phone_number = PhoneNumberValidators(null=False)
    detail = models.CharField(max_length=255,null=False)
    city = models.CharField(max_length=20,null=False)
    district = models.CharField(max_length=20,null=False)
    commune = models.CharField(max_length=30,null=False)
    type = models.CharField(
        max_length=50, choices=ADDRESS_TYPE, default="other"
    )  # Home, Work, Other
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        #the first address always has is_default=True
        if not Address.objects.filter(user=self.user).exists():
            self.is_default = True
        else:
            if self.is_default:
                Address.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
            if not Address.objects.filter(is_default=True).exists():
                self.is_default=True
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'addresses'
        verbose_name_plural = "Addresses"


def to_kebab_case(input_string):
    return input_string.replace(" ", "-").lower()

class Movie(models.Model):
    RATING_TYPE = (('g','G'),('pg','PG'),('pg-13','PG-13'),('r','R'))
    title = models.CharField(max_length=100,null=False)
    release_date = models.DateField(null=False,default='1980-01-01')
    end_point = models.CharField(max_length=300,null=True,blank=True)
    runtime = models.IntegerField(null=False,default=0)
    movie_url = models.FileField(upload_to='documents/')
    synopsis = models.TextField(null=True,blank=True)
    mpaa_rating = models.CharField(choices=RATING_TYPE,default='g',null=False,max_length=5)
    score = models.DecimalField(max_digits=3, decimal_places=1,null=False)
    imdb_score = models.DecimalField(max_digits=3, decimal_places=1, null=False)

    def __str__(self) -> str:
        return self.title
    
    def generate_unique_endpoint(self):
        return f"{to_kebab_case(self.title)}-{uuid.uuid4()}"
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            return total_rating / reviews.count()
        else:
            return None

    def save(self,*args,**kwargs):
        if not self.end_point:
            self.end_point = self.generate_unique_endpoint()
        super(Movie, self).save(*args, **kwargs)
    class Meta:
        managed = True
        db_table = 'movies'
        verbose_name_plural = "Movies"

class MovieImage(models.Model):
    IMAGE_TYPE = (('poster','Poster'),('backdrop','Backdrop'),('screenshot','Screenshot'))
    movie = models.ForeignKey(Movie, models.CASCADE,related_name='images')
    image_url = models.ImageField(upload_to="images/movie_images/")
    type = models.CharField(choices=IMAGE_TYPE,default='backdrop',null=False,max_length=15)


    @property
    def image(self):
        if self.image_url:
            return self.image_url.url
        return static("images/default/default_movie_image.png")
    def __str__(self) -> str:
        return self.movie.title
    
    class Meta:
        managed = True
        db_table = 'movie_images'
        verbose_name_plural = "Movie Images"

class Genre(models.Model):
    name = models.CharField(unique=True,default='',max_length=20)

    class Meta:
        managed = True
        db_table = 'genres'
        verbose_name_plural = "Genres"

class Cast(models.Model):
    CAST_ROLE = (('actor','Actor'),('director','Director'))
    name = models.CharField(max_length=100)
    dob = models.DateField(blank=True, null=True)
    role = models.CharField(choices=CAST_ROLE,default='actor',null=False,max_length=10)
    ranking = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    class Meta:
        managed = True
        db_table = 'casts'
        verbose_name_plural = "Casts"


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, models.CASCADE)
    cast = models.ForeignKey(Cast, models.CASCADE)

    def __str__(self) -> str:
        return f'{self.movie.title} - {self.cast.name}'
    class Meta:
        managed = True
        db_table = 'movie_cast'
        verbose_name_plural = "Movie Casts"
        # unique_together = ('movie','cast')


class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE,related_name='reviews')
    movie = models.ForeignKey(Movie, models.CASCADE,related_name='reviews')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    total_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self) -> str:
        return self.user.profile.display_name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update movie average rating when a review is saved
        self.movie.save()

    class Meta:
        managed = True
        db_table = 'reviews'
        verbose_name_plural = "Reviews"


class Watchlist(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    movie = models.ForeignKey(Movie, models.CASCADE,related_name='watchlists')

    class Meta:
        managed = True
        db_table = 'watchlists'
        verbose_name_plural = "Watch Lists"




class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, models.CASCADE)
    genres = models.ForeignKey(Genre, models.CASCADE)

    class Meta:
        managed = True
        db_table = 'movie_genres'
        unique_together = ('movie', 'genres')
        verbose_name_plural = "Movie Genres"

