"""
URL configuration for Records project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView ,PasswordResetCompleteView


from setting.views import UserDetailView

app_name = 'records'

urlpatterns = [
    path('user/password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('user/password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('', include('industry.urls')),
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('user_profile/<uuid:pk>', UserDetailView.as_view(),name='user_profile'),
    path('user/', include('authentication.urls')),
    path('settings/', include('setting.urls')),
]
