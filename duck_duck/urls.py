from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('secret_messages.urls')),
    path('economics/', include('economics.urls')),
    path('', include('food_menu.urls')),
    path('holidays/', include('holidays.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('mining/', include('mining.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
