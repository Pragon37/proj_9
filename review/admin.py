from django.contrib import admin
from .models import Ticket
from .models import Review

admin.site.register(Ticket)
admin.site.register(Review)
