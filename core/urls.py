from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('error/', views.PageErrorView.as_view(), name='restricted'),
]