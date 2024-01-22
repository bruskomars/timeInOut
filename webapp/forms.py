from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import User, TimeInOut
from datetime import datetime

from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.forms import widgets


# Register
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


# Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Add Time In Out
class TimeInOutForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(TimeInOutForm, self).__init__(*args, **kwargs)
    #     self.fields['time_start'] = forms.TimeField(initial=datetime.now().strftime('%I:%M %p'))
    #     self.fields['time_start'].disabled = True

    class Meta:
        model = TimeInOut
        fields = '__all__'
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'time_start': widgets.TimeInput(attrs={'type': 'time'}),
            'time_end': widgets.TimeInput(attrs={'type': 'time'}),
        }
