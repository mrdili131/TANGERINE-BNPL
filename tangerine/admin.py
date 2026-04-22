from django.contrib import admin
from .models import *

admin.site.register([
    Shop,
    Client,
    Application,
    Contract,
    PhoneNumber
])