from django.contrib.auth.models import User

from rest_framework import viewsets

from example.serializers import UserSerializers, BookSerializer
from example.models import Book


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
