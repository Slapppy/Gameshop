from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from source.models import User


class ProfileForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect password.")
        return password

    def save(self):
        self.user.email = self.cleaned_data["email"]
        if self.cleaned_data["new_password"]:
            self.user.set_password(self.cleaned_data["new_password"])
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.save()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["password", "email", "first_name", "last_name"]


class AddGameForm(forms.Form):
    game_id = forms.IntegerField(label="Game ID")
    price = forms.DecimalField(max_digits=8, decimal_places=2)
