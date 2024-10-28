from django.contrib import admin
from .models import *

admin.site.register((Church,Member,ChurchRecord,Offering,Service))
# Register your models here.
