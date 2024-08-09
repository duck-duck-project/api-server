from django.http import HttpResponse


class OkTrueMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response: HttpResponse = self.get_response(request)

        return response
