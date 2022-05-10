from django import forms

from .constants import SEARCH_IGNORE, SEARCH_ALL
from .models import Device


class DeviceAddForm(forms.ModelForm):
    """Form to be used for adding new Devices."""

    class Meta:
        model = Device
        exclude = ['added_on']
        widgets = {
            'added_by': forms.HiddenInput()
        }


class DeviceFilterForm(forms.Form):
    """Form to use for searching or filtering devices"""

    search_keyword = forms.CharField(label='Keyword', min_length=2, max_length=150, required=False)
    time_sort = forms.ChoiceField(label='Sort by Date', choices={
        (SEARCH_IGNORE, '-----'),
        ("added_on", "Oldest First"),
        ("-added_on", "Newest First"),
    }, initial=SEARCH_IGNORE)
    price_sort = forms.ChoiceField(label='Sort by Price', choices={
        (SEARCH_IGNORE, '-----'),
        ("-price", "High To Low"),
        ("price", "Low To High"),
    }, initial=SEARCH_IGNORE)

    FILTER_DEVICE_TYPE_CHOICES = [(SEARCH_ALL, '-----')] + Device.DEVICE_TYPE_CHOICES
    device_type_search = forms.ChoiceField(choices=FILTER_DEVICE_TYPE_CHOICES, initial=SEARCH_ALL, label='Device Type')
