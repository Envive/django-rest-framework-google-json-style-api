from rest_framework import routers

from example.views import (
    AuthorViewSet,
    BookViewSet,
    UserViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
urlpatterns = router.urls
