from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse

from devices.models import Device
from user_profile.models import Notification
from .signals import custom_post_save


@receiver(custom_post_save)
def recommend_device_based_on_likes(sender, **kwargs):
    """Send notifications to the users with similar liked items.

    Args:
        sender: The class calling the function

    Returns:
        None
    """
    added_device = kwargs['device']
    related_devices = Device.objects.filter(device_type=added_device.device_type)
    related_user_ids = set(related_devices.values_list('userprofile__user_id', flat=True))

    for user_id in related_user_ids:
        if user_id is not None:
            device_url = reverse('display-device', kwargs={'pk': added_device.id})
            messgae = f'<b>{added_device.added_by.username}</b> added a new device.' \
                      f'Be sure to check it out at <a href="{device_url}">{added_device.name}</a>'
            Notification.objects.create(recipient=User.objects.get(id=user_id), message=messgae)
