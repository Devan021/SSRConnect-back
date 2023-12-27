from rest_framework import generics

from core.permissions import IsAdmin, IsMentor
from user.models import Team
from user.serializers import AdminUserSerializer, AdminTeamSerializer


class TeamCreate(generics.CreateAPIView):
    serializer_class = AdminTeamSerializer
    queryset = Team.objects.all()


class TeamList(generics.ListAPIView):
    permission_classes = [IsMentor]
    serializer_class = AdminTeamSerializer
    queryset = Team.objects.all()


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AdminUserSerializer
    queryset = Team.objects.all()


__all__ = [
    'TeamCreate',
    'TeamList',
    'TeamDetail',
]
