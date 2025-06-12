from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


def email_exist(email):
    if not email:
        raise ValidationError('Email field is required')
    
def email_not_exist_validator(mail):
    """Validator that checks if email is not already in use"""
    mail = get_user_model().objects.filter(email=mail)
    if not mail.exists():
        raise ValidationError(f"There is no account with this email")