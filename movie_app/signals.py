from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.utils import timezone
from .models import Genre

@receiver(user_logged_in)
def update_last_login(sender,user,request,**kwargs):
    user.last_login = timezone.now()
    user.save()


@receiver(post_migrate)
def create_genre(sender,**kwargs):
    GENRE_LIST = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Superhero', 'Thriller', 'War', 'Western']
    existing_genres = Genre.objects.values_list('name',flat=True)
    genre_to_create = [genre for genre in GENRE_LIST if genre not in existing_genres]
    for genre_name in genre_to_create:
        Genre.objects.create(name=genre_name)