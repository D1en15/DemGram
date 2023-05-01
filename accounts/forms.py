from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    SetPasswordForm
)
from django import forms
from typing import Any
from accounts.tasks import send_verification_email
from accounts.models import User


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class PasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-group",
            }
        )
    )
    username = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-group",
            }
        )
    )

    class Meta:
        model = User
        fields = ("username", "password")


class RegistrationForm(UserCreationForm):
    attrs = {"class": "form-group"}
    username = forms.CharField(widget=forms.TextInput(attrs=attrs))
    email = forms.EmailField(widget=forms.EmailInput(attrs=attrs))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True) -> Any:
        user = super(RegistrationForm, self).save(commit=True)
        send_verification_email.delay(user_id=user.id)
        return user


class EmailChangeForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-group"}))


class DeadlineEmailTimeForm(forms.Form):
    time = forms.IntegerField(widget=forms.NumberInput(), required=False)


class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(), required=True)