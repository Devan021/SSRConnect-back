from user.authentication import CookieTokenAuthentication, set_token_cookies


def handle_refresh_token(func):

    def wrapper(self, request, *args, **kwargs):
        print("handle_refresh_token")
        response = func(self, request, *args, **kwargs)
        user, tokens = CookieTokenAuthentication().authenticate(request)
        if tokens:
            response = set_token_cookies(response, tokens['ACCESS_TOKEN'], tokens['REFRESH_TOKEN'])
        print("handle_refresh_token", response)
        return response

    return wrapper


__all__ = [
    'handle_refresh_token'
]
