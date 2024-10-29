from django.core.exceptions import ValidationError

def email_exist(email):
    if not email:
        raise ValidationError('Email field is required')