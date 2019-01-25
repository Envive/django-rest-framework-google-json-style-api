from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from example.models import Author, Book
from example.serializers import (
    AuthorNameSerializer,
    BookSerializer,
    UserSerializers
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('pk').all()
    serializer_class = UserSerializers


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        return BookSerializer

    def get_object(self):
        # Handle featured
        entry_pk = self.kwargs.get('entry_pk', None)
        if entry_pk is not None:
            return Book.objects.exclude(pk=entry_pk).first()

        return super(BookViewSet, self).get_object()


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()

    def get_serializer_class(self):
        return AuthorNameSerializer

    def list(self, request, *args, **kwargs):
        response = super(AuthorViewSet, self).list(request, *args, **kwargs)
        response.data = {
            'meta': {
                'num_author': self.queryset.count(),
            },
            'results': response.data
        }
        return response


class NoStatusCodeView(APIView):

    def get(self, request, format=None):
        response = Response()
        del response.status_code
        return response
