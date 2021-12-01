from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from app.userprofile.models import Profile
User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
