from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User


class ProfileView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'name': user.name,
        }, status=200)


class UpdateProfileView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if data.get("name"):
            user.name = data.get("name")
        if data.get("avatar"):
            user.avatar = data.get("avatar")
        if data.get("email"):
            if User.objects.filter(email=data.get('email')).exists():
                return Response({
                    'error': {
                        'code': "EMAIL_ALREADY_EXISTS",
                        'message': 'Email already exists'
                    },
                }, status=400)
            user.email = data.get("email")
        user.save()
        return Response({
            'id': user.id,
            'email': user.email,
            'name': user.name,
        }, status=200)


__all__ = [
    'ProfileView',
    'UpdateProfileView',
]
