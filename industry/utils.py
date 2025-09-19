import re

from django.contrib.auth import get_user_model
from django.db.models import Q

from bible.utils import Bible

def search_users(search):
    return get_user_model().objects.filter(
        Q(first_name__icontains=search)|
        Q(last_name__icontains=search)|
        Q(username__icontains=search)
    )

def setup_context(request, members, services, main_context):
    search_type = request.GET['type']
    data = request.GET['q']
    context = {'church':''}

    if data == '':
        return main_context

    if search_type == 'service':
        context['services'] = services.filter(name__icontains=data)
    elif search_type == 'member':
        members = members.filter(
            Q(first_name__icontains=data)|
            Q(last_name__icontains=data)
        )
        context['members'] = members
    return context

def split_passage(passage):
        pattern = r"^([\d]?\s?[A-Za-z ]+)\s+(\d+):(\d+)(?:-(\d+))?$"
        match = re.match(pattern, passage.strip())

        if not match:
            raise ValueError(f"Invalid passage format: {passage}")

        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse1 = int(match.group(3))
        verse2 = int(match.group(4)) if match.group(4) else 0

        return book, chapter, verse1, verse2


def prep_text(text):
    book,chapter,verse1,verse2 = split_passage(text)
    passage = Bible(book,chapter,verse1,verse2)
    return passage
