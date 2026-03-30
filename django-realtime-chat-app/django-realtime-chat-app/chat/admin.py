from django.contrib import admin
from .models import Message, UserPresence, Notification

admin.site.register(Message)
admin.site.register(UserPresence)
admin.site.register(Notification)
