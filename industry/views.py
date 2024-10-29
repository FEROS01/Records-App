from django.shortcuts import render


from .models import Church


def index(request):
    return render(request, 'industry/index.html')