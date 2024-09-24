from django.conf import settings
from django.contrib import admin
from django.urls import include, path

ROOT_PATH = ''

urlpatterns = [
    path(f'{ROOT_PATH}admin/', admin.site.urls),
    path(f'{ROOT_PATH}', include('users.urls')),
    path(f'{ROOT_PATH}secret-messages/', include('secret_messages.urls')),
    path(f'{ROOT_PATH}economics/', include('economics.urls')),
    path(f'{ROOT_PATH}', include('food_menu.urls')),
    path(f'{ROOT_PATH}holidays/', include('holidays.urls')),
    path(f'{ROOT_PATH}quizzes/', include('quizzes.urls')),
    path(f'{ROOT_PATH}mining/', include('mining.urls')),
    path(f'{ROOT_PATH}relationships/', include('relationships.urls')),
    path(f'{ROOT_PATH}', include('user_characteristics.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
