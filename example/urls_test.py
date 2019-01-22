from rest_framework import routers

from example.views import (
    BookViewSet,
    UserViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
urlpatterns = router.urls
