from datetime import datetime, timedelta

from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def set_token_cookies(response, access_token, refresh_token):
    response.set_cookie(
        key='ACCESS_TOKEN',
        value=access_token,
        expires=datetime.now() + timedelta(hours=1),
        samesite=False,
        httponly=True,
    )
    response.set_cookie(
        key='REFRESH_TOKEN',
        value=refresh_token,
        expires=datetime.now() + timedelta(days=30),
        samesite=False,
        httponly=True,
    )
    return response


class CookieTokenAuthentication(BaseAuthentication):
    """
    Token-based authentication using cookies.
    """

    def authenticate(self, request):
        access_token = request.COOKIES.get('ACCESS_TOKEN')
        refresh_token = request.COOKIES.get('REFRESH_TOKEN')
        if not access_token and not refresh_token:
            return None, None
        authentication = JWTAuthentication()
        print("access_token", access_token)
        print("refresh_token", refresh_token)

        try:
            if access_token:
                validated_token = authentication.get_validated_token(access_token)
                user = authentication.get_user(validated_token)
                return user, None
        except AuthenticationFailed:
            print("AuthenticationFailed")
            pass

        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
                access_token = str(refresh_token.access_token)
                user = authentication.get_user(refresh_token)
                return user, {
                    "ACCESS_TOKEN": access_token,
                    "REFRESH_TOKEN": refresh_token,
                }
            except Exception:
                print("AuthenticationFailed2")
                pass

        print("AuthenticationFailed3")
        return None, None


__all__ = [
    'CookieTokenAuthentication',
    'set_token_cookies'
]
