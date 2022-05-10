from django.urls import path

from . import views

urlpatterns = [

    path('', views.landing_view, name='landing-page'),

    path('device/add', views.AddDevice.as_view(), name='add-device'),
    path('device/<int:pk>', views.DisplayDevice.as_view(), name='display-device'),
    path('device', views.DeviceList.as_view(), name='list-device'),
    path('device/add-fav/<int:pk>', views.toggle_device_like, name='like-device'),
    path('device/favs', views.liked_devices, name='liked-device'),
    path('device/added', views.added_devices, name='added-device'),
    path('device/update/<int:pk>', views.UpdateDevice.as_view(), name='update-device'),
    path('device/delete/<int:pk>', views.DeleteDevice.as_view(), name='delete-device'),

]
