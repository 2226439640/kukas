from django.shortcuts import render, redirect
from caseManage.models import Users


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        if not username or not pwd:
            return render(request, 'login.html', {'msg': '用户信息不能为空!'})
        user = Users.objects.filter(name=username, password=pwd).first()
        if user:
            request.session['username'] = username
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg': '用户信息错误!'})
    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return render(request, 'login.html')
