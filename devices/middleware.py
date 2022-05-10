import re

from django.db.models import F
from django.utils.deprecation import MiddlewareMixin

from devices.models import DeviceHit


class DeviceHitCounterMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """Increments the device visit counter each time it is requested by the user."""
        request_url = request.get_full_path()
        item_detail_url = re.match(r'/smart_electronics/(\d+)', request_url)

        if item_detail_url:
            item_id = item_detail_url.group(1)
            item_hit, _ = DeviceHit.objects.get_or_create(item_id=item_id)
            item_hit.hits = F('hits') + 1
            item_hit.save()
