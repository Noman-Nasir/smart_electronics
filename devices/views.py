from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, DetailView, UpdateView, DeleteView

from .constants import SEARCH_IGNORE, SEARCH_ALL
from .forms import DeviceAddForm, DeviceFilterForm
from .models import Device


def landing_view(request):
    """Renders the home page for site users.

    Args:
        request: WSGIRequest 
    """
    context = dict()
    if Device.objects.count() > 1:
        newest_devices = Device.objects.all().order_by('-added_on')[:5]
        context = {
            'latest_devices': newest_devices[1:],
            'active_device': newest_devices[0],
        }
    return render(request, 'landing_page.html', context=context)


@login_required
def liked_devices(request):
    """Filters the devices liked by the user.

    Args:
        request: WSGIRequest
    """
    return render(request, 'device/personal_list.html', context={
        'devices': request.user.profile.liked_devices.all(),
        'page_title': 'Liked Devices',
    })


@login_required
def added_devices(request):
    """Filters the devices Added by the user.

    Args:
        request: WSGIRequest
    """
    return render(request, 'device/personal_list.html', context={
        'devices': Device.objects.filter(added_by=request.user),
        'page_title': 'Added Devices',
    })


@login_required
@require_http_methods(["POST"])
def toggle_device_like(request, pk):
    """Toggles device like for the given device pk.

    Args:
        request: WSGIRequest
        pk: Id of the deivce.
    """

    if request.user.profile.liked_devices.filter(id=pk).count():
        request.user.profile.liked_devices.remove(Device.objects.get(pk=pk))
    else:
        request.user.profile.liked_devices.add(Device.objects.get(pk=pk))

    return redirect(reverse('list-device'))


class AddDevice(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'device/add.html'
    form_class = DeviceAddForm

    def form_valid(self, form):
        form.save()
        return redirect(reverse('list-device'))

    def test_func(self):
        """Checks if the user is a seller or not

        Returns:
        bool: True is user is a seller else False
        """
        return self.request.user.profile.is_seller


class DeleteDevice(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'device/delete.html'
    model = Device

    def get_success_url(self):
        return reverse_lazy('list-device')

    def __is_cancel_request(self):
        """Checks if user has cancelled delete request

        Returns:
        bool: True is user has cancelled the request else False
        """
        if "cancel" in self.request.POST:
            return True
        return False

    def post(self, request, *args, **kwargs):
        if self.__is_cancel_request():
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(DeleteDevice, self).post(request, *args, **kwargs)

    def test_func(self):
        """Checks if the user is a seller or not

        Returns:
        bool: True is user is a seller else False
        """
        return self.request.user.profile.is_seller


class UpdateDevice(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'device/update.html'
    model = Device
    fields = ['name', 'price', 'description', 'manufacturer']

    def get_success_url(self):
        return reverse_lazy('list-device')

    def test_func(self):
        """Checks if the user is a seller or not

        Returns:
        bool: True is user is a seller else False
        """
        return self.request.user.profile.is_seller


class DeviceList(FormView):
    form_class = DeviceFilterForm
    template_name = "device/list.html"

    def __apply_search_filter(self, search, queryset):
        """Applies specified filtering parameters on given queryset

        Args:
            search: dict object containing filtering parameters
            queryset: queryset to Apply filtering on

        Returns:
            Filtered queryset
        """
        keyword = search['search_keyword']
        device_type = search['device_type_search']
        time_sort = search['time_sort']
        price_sort = search['price_sort']

        queryset = queryset.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) |
                                   Q(manufacturer__icontains=keyword))

        if device_type != SEARCH_ALL:
            queryset = queryset.filter(device_type=device_type)

        if time_sort != SEARCH_IGNORE and price_sort != SEARCH_IGNORE:
            queryset = queryset.order_by(time_sort, price_sort)
        elif time_sort == SEARCH_IGNORE and price_sort != SEARCH_IGNORE:
            queryset = queryset.order_by(price_sort)
        elif time_sort != SEARCH_IGNORE and price_sort == SEARCH_IGNORE:
            queryset = queryset.order_by(time_sort)

        return queryset

    def get_context_data(self, **kwargs):
        """Overrides built-in get_context_data function.

        Overrides built-in func to add page title and Id's of liked devices
        and order queryset in descending order by date.

        Returns:
        New context dictionary
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All Devices'
        context['devices'] = Device.objects.all().order_by('-added_on')

        if self.request.user.is_authenticated:
            context['liked_devices_id'] = self.request.user.profile.liked_devices.all().values_list('id', flat=True)

        return context

    def form_valid(self, form, **kwargs):
        """Applies filtering parameters specified in the form

        Args:
            form: User submitted HTML form
        """
        context = dict()
        context['page_title'] = 'Filtered Devices'
        context['devices'] = self.__apply_search_filter(form.cleaned_data, Device.objects.all())
        if self.request.user.is_authenticated:
            context['liked_devices_id'] = self.request.user.profile.liked_devices.all().values_list('id', flat=True)

        return render(self.request, 'device/list.html', context=context)


class DisplayDevice(DetailView):
    model = Device
    template_name = 'device/detail.html'
