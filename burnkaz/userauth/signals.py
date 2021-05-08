import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from .models import User

logger = logging.getLogger(__name__)
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        logging.info('User created')

