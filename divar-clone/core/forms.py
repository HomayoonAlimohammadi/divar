from django import forms
from core.models import Item
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password_conf = forms.CharField(
        widget=forms.PasswordInput, label="Password Confimation"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
        ]


class UserUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=256, required=False)
    last_name = forms.CharField(max_length=256, required=False)
    username = forms.CharField(max_length=256, required=False)
    email = forms.EmailField(max_length=256, required=False)
    password = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput
    )
    password_conf = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.PasswordInput,
        label="Password Confirmation",
    )


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ["user"]
