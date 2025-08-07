from django.forms import ModelForm
from .models import Room, Topic, User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ["host", "participants"]
        widgets = {
            "topic": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]  # Add any other fields you want to allow users to


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"
