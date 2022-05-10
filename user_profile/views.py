from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView

from user_profile.forms import UserCreationForm


@login_required
def profile_view(request):
    """Renders user profile"""
    return render(request, 'user/profile.html')


class RegisterUser(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        """Registers and login a new user.

        Args:
            form: User submitted HTML form
        """
        form.save()
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)

        return redirect(reverse('user-profile'))


@login_required
def notifications(request):
    return render(request, 'notifications/list.html', context={
        'notifications': request.user.profile.get_unread_notifications_and_mark_read(),
    })

