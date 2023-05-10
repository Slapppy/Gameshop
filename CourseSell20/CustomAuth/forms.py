from django import forms
from django.contrib.auth.forms import UserCreationForm
from source.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
