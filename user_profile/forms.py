from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user_profile.models import UserProfile


class UserCreationForm(forms.ModelForm):
    """Form used for adding new Users"""
    username = forms.CharField(label='Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(min_length=3, max_length=50)
    last_name = forms.CharField(min_length=3, max_length=50)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'avatar', 'date_of_birth',
                  'is_seller', ]
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(1960, 2011)),
        }

    def save(self, commit=True):

        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

        custom_user = UserProfile.objects.create(
            user=user,
            avatar=self.cleaned_data['avatar'],
            is_seller=self.cleaned_data['is_seller'],
            date_of_birth=self.cleaned_data['date_of_birth']
        )

        return custom_user

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).count():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2
