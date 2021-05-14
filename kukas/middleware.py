from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from caseManage.updateFile import updateFile


class loginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'login' not in request.path_info and not request.session.get('username'):
            return render(request, 'login.html')

    @staticmethod
    def _contains(strPath, args):
        for i in args:
            if strPath.find(i) != -1:
                return True
        return False

    def process_response(self, request, response):
        if self._contains(request.path_info, ['uploadcase', 'updatecase', 'delcase']):
            update = updateFile()
            update(fileFlag=True, user_id=request.session["userid"])
        return response