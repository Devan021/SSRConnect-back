from django.db.models import Q
from rest_framework import generics

from core.permissions import IsAdmin, IsMentor
from user.models import User
from user.serializers import AdminUserSerializer, ChangePasswordSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()


class UserList(generics.ListAPIView):
    permission_classes = [IsMentor]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        keyword = self.request.query_params.get('q')
        if keyword is not None:
            queryset = queryset.filter(Q(name__contains=keyword) or Q(email__contains=keyword))
        return queryset


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()


class UserChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.kwargs['id'])


__all__ = [
    'UserCreate',
    'UserList',
    'UserDetail',
    'UserChangePassword'
]
