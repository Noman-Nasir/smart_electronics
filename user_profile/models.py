from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models

from devices.models import Device


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_notification')
    message = models.TextField()
    read = models.BooleanField(default=False)
    recieved_date = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars', verbose_name='Profile Pic')
    is_seller = models.BooleanField(verbose_name='Register As a Seller')
    date_of_birth = models.DateField()
    liked_devices = models.ManyToManyField(Device)

    def __str__(self):
        return self.user.username

    def get_unread_notifications_count(self):
        return Notification.objects.filter(recipient=self.user, read=False).count()

    def get_unread_notifications_and_mark_read(self):
        """Returns unread notifications.

        Returns unread notifications for the user and if mark_read
        is True. It marks them as read otherwise leaves them as unread.
        """
        if Notification.objects.filter(recipient=self.user).exists():
            notifications = list(Notification.objects.filter(recipient=self.user).order_by('-recieved_date'))
            Notification.objects.filter(recipient=self.user, read=False).update(read=True)
            return notifications
        else:
            return None
