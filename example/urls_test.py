from rest_framework import routers

from example.views import (
    UserViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
urlpatterns = router.urls
