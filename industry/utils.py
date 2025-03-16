from django.contrib.auth import get_user_model
from django.db.models import Q

def search_users(search):
    return get_user_model().objects.filter(
        Q(first_name__icontains=search)|
        Q(last_name__icontains=search)|
        Q(username__icontains=search)
    )