from django import forms


class UserCreateUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    username = forms.CharField(max_length=128)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_conf = forms.CharField(widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)


class ItemCreateForm(forms.Form):
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea, required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    image = forms.ImageField(required=False)
