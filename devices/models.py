from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from .signals import custom_post_save


class Device(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(verbose_name='Price($)')
    image = models.ImageField(upload_to='images/', verbose_name='Device Image')
    LAPTOP = 'LP'
    MOBILE = 'MB'
    MOBILE_ACCESSORY = 'MA'
    LAPTOP_ACCESSORY = 'LA'
    OTHER = 'OT'

    DEVICE_TYPE_CHOICES = [
        (LAPTOP, 'Laptop'),
        (MOBILE, 'Mobile'),
        ('Accessory', (
            (MOBILE_ACCESSORY, 'Mobile Accessory'),
            (LAPTOP_ACCESSORY, 'Laptop Accessory'),
        )),
        (OTHER, 'Other')
    ]
    device_type = models.CharField(max_length=2, choices=DEVICE_TYPE_CHOICES, default=MOBILE)
    description = models.TextField(max_length=500)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    added_on = models.DateTimeField(default=now)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super(Device, self).save(*args, **kwargs)
        custom_post_save.send_robust(sender=self.__class__, device=self)


class DeviceHit(models.Model):
    """Keeps a count of how many times an individual device has been visited by users."""
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    hits = models.PositiveIntegerField(default=0)
