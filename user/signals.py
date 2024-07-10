from django.db.models.signals import post_save
from django.dispatch import receiver
from movie_app.models import Address

@receiver(post_save,sender = Address)
def set_default_address(sender,instance,created,**kwargs):
    if created and instance.is_default:
        # If the instance being saved is newly created and marked as default
        Address.objects.filter(user=instance.user).exclude(pk=instance.pk).update(is_default=False)
    elif not Address.objects.filter(user=instance.user, is_default=True).exists():
        # If no other address is marked as default, set the first one as default
        addresses = Address.objects.filter(user=instance.user)
        if addresses.exists():
            first_address = addresses.first()
            first_address.is_default = True
            first_address.save()