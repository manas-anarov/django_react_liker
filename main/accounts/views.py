from .serializers import RegisterSerializer

from rest_framework.generics import (CreateAPIView)

from rest_framework.permissions import (
    AllowAny,
)

from django.contrib.auth.models import User


class Register(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
