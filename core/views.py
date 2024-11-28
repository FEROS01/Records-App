from django.shortcuts import render
from django.views.generic import TemplateView

class PageErrorView(TemplateView):
    template_name = 'core/error.html'
