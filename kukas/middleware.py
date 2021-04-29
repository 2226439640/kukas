from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render


class loginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session['username']:
            return render(request, 'login/')