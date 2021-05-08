import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from developer.models import Developer, DeveloperService, Favorites
from userauth.models import User

@receiver(post_save, sender=Developer)
def developer_created(sender, instance, created, **kwargs):
    if created:
        DeveloperService.objects.create(
            service_title=instance.service_title,
            service_description=instance.service_description,
            price=instance.price,
            price_fix=instance.price_fix
        )

@receiver(post_delete, sender=Favorites)
def favorite_bool(sender, instance, **kwargs):
    if instance.favorite_bool == False:
        Favorites.objects.get(developer=instance.developer).delete()
