from django.contrib.auth import get_user_model
from django.db.models import Q

def search_users(search):
    return get_user_model().objects.filter(
        Q(first_name__icontains=search)|
        Q(last_name__icontains=search)|
        Q(username__icontains=search)
    )

def setup_context(request, church, main_context):
    search_type = request.GET['type']
    data = request.GET['q']
    context = {'church':''}

    if data == '':
        return main_context

    if search_type == 'service':
        services = church.service.filter(name__icontains=data)
        context['services'] = services
    elif search_type == 'member':
        members = church.members.filter(
            Q(first_name__icontains=data)|
            Q(last_name__icontains=data)
        )
        context['members'] = members
    return context