from user.decorators import handle_refresh_token


class RefreshTokenMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    @handle_refresh_token
    def __call__(self, request):
        response = self.get_response(request)
        return response
