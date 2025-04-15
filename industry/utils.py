from django.contrib.auth import get_user_model
from django.db.models import Q

def search_users(search):
    return get_user_model().objects.filter(
        Q(first_name__icontains=search)|
        Q(last_name__icontains=search)|
        Q(username__icontains=search)
    )

def setup_context(request, church):
    search_type = request.GET['type']
    data = request.GET['q']
    if search_type == 'service':
        services = church.service.filter(name__icontains=data)
        return {'services':services}
    elif search_type == 'member':
        members = church.members.filter(
            Q(first_name__icontains=data)|
            Q(last_name__icontains=data)
        )
        return {'members':members}
    return {}