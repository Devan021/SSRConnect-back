from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from user.authentication import set_token_cookies
from user.serializers import CookieTokenAuthenticationSerializer


class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CookieTokenAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_data = response.data
        print(response.data)
        access_token = token_data['access']
        refresh_token = token_data['refresh']
        response = Response(status=200)
        set_token_cookies(response, access_token, refresh_token)
        response.data = {
            'message': 'Login successfully'
        }
        return response


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CookieTokenAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        for field in ['email', 'name', 'password']:
            if not data.get(field):
                return Response({
                    'error': {
                        'code': "MISSING_FIELD",
                        'message': f'{field} is required'
                    },
                }, status=400)
        if User.objects.filter(email=data.get('email')).exists():
            return Response({
                'error': {
                    'code': "EMAIL_ALREADY_EXISTS",
                    'message': 'Email already exists'
                },
            }, status=400)
        if not data.get('email').endswith('amrita.edu'):
            return Response({
                'error': {
                    'code': "INVALID_EMAIL",
                    'message': 'Email must be amrita.edu domain'
                },
            }, status=400)
        user = User.objects.create_user(
            email=data.get('email'),
            name=data.get('name'),
            username=data.get('email'),
        )
        user.set_password(data.get('password'))
        user.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = Response(status=200)
        set_token_cookies(response, access_token, refresh)
        response.data = {
            'message': 'Registration success'
        }
        return response


class UserLogoutView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response = Response(status=200)
        response.delete_cookie('ACCESS_TOKEN')
        response.delete_cookie('REFRESH_TOKEN')
        response.data = {
            'message': 'Logout successfully'
        }
        return response


__all__ = [
    'UserRegisterView',
    'UserLoginView',
    'UserLogoutView',
]
