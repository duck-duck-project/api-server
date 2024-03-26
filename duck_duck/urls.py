from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('secret_messages.urls')),
    path('economics/', include('economics.urls')),
    path('', include('food_menu.urls')),
    path('manas-id/', include('manas_id.urls')),
    path('holidays/', include('holidays.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
