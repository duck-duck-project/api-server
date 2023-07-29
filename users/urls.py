from rest_framework.routers import DefaultRouter

from users.views import UserApi

router = DefaultRouter()
router.register('', UserApi, basename='user')

urlpatterns = router.urls
