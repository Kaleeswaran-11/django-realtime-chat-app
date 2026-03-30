from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('', lambda request: redirect('chat:dashboard')),
    path('chat/', include('chat.urls')),
]
