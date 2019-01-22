from django.contrib.auth.models import User

from rest_framework import viewsets

from example.serializers import UserSerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('pk').all()
    serializer_class = UserSerializers
