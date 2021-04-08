from django.shortcuts import render, redirect
from login import models

# Create your views here.

def index(request):
    if not request.session.get('is_login', None):
        login = False
        return render(request, 'home/index.html', locals())

    login = True
    user_id = request.session.get('user_id')
    user = models.User.objects.get(id=user_id)
    detail = models.UserDetail.objects.filter(user=user)
    if detail:
        avatar = detail[0].avatar
    else:
        avatar = 'img/renge.jpg'
    # print(avatar)
    return render(request, 'home/index.html', locals())


def logout(request):
    # 如果没有登录的话，那就去登录吧
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect('/login/')


def test(request):
    pass
