from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CookieTokenAuthenticationSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_name'] = user.name
        token['user_email'] = user.email
        if user.is_superuser:
            token['user_type'] = 'ADMIN'
        elif user.is_staff:
            token['user_type'] = 'MENTOR'
        else:
            token['user_type'] = 'STUDENT'
        return token


__all__ = [
    'CookieTokenAuthenticationSerializer'
]
