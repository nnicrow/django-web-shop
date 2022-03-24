from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Users


class UsersCreationForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('email', 'username', 'password', 'first_name', 'last_name',)


class UsersChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ('email', 'username', 'password', 'first_name', 'last_name',)
