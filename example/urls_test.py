from django.urls import path

from rest_framework import routers

from example.views import (
    AuthorViewSet,
    BookViewSet,
    UserViewSet,
    NoStatusCodeView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('no_status', NoStatusCodeView.as_view()),
]
