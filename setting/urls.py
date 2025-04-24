from django.urls import path

from . import views

app_name = 'setting'

urlpatterns = [
    path('settings/',views.SettingView.as_view(),name='settings'),
    path('user_update/<uuid:pk>',views.UserUpdateView.as_view(),name='user_update')
]