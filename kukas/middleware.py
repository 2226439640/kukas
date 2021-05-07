from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render


class loginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'login' not in request.path_info and not request.session.get('username'):
            return render(request, 'login.html')