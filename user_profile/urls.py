from django.urls import path

from user_profile import views

urlpatterns = [

    path('register', views.RegisterUser.as_view(), name="register"),
    path('profile', views.profile_view, name='user-profile'),
    path('notifications', views.notifications, name='display-notification')
]
