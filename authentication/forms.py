from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth import get_user_model

from .validators import email_not_exist_validator

class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email')

class NewPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        email_field = self.fields['email']
        email_field.validators.append(email_not_exist_validator)