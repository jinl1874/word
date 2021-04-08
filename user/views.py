import django
import login.models
from check.models import Check
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import InvalidPage, PageNotAnInteger, Paginator

from user.models import ChangeDetail, Dynamics, UserChange, UserWord

from .form import *


# Create your views here.
def user(request):
    if not request.session.get('is_login', None):
        Login = False
        message = '还未登录，请前往登录！'
        return render(request, 'buff.html', locals())
    username = request.session.get('user_name')
    return redirect('/user/{}/'.format(username))


def user_info(request, username):
    try:
        user = login.models.User.objects.get(username=username)
    except:
        return render(request, 'error.html', locals())

    try:
        user_detail = login.models.UserDetail.objects.get(user=user)
    except:
        user_detail = login.models.UserDetail(user=user, nickname=username, sex='其它', sign='这个人很懒，什么也没有留下')
        user_detail.save()
    try:
        user_word = UserWord.objects.get(username=username)
    except:
        user_word = UserWord()
        user_word.username = username
        user_word.word_type = 'cet-4'
        user_word.save()

    word_type = user_word.word_type
    avatar = user_detail.avatar

    dynamicses = Dynamics.objects.filter(username=username)
    checks = Check.objects.filter(username=username)
    word_num = 0
    for c in checks:
        word_num += c.check_num
    note_num = 1
    check_num = len(checks)
    return render(request, 'user/user.html', locals())
    # dynamics_pages = Paginator(dynamicses, 10)
    # check_pages = Paginator(checks, 10)
    # if request.method == 'GET':
    #     dynamicses = dynamics_pages.page(1)
    #     checks = check_pages.page(1)
    #     return render(request, 'user/user.html', locals())
    # if request.is_ajax():
    #     page = request.GET.get('page')
    #     try:
    #         dynamicses = dynamics_pages.page(page)
    #     # 如果页数不是整数，返回第一页
    #     except PageNotAnInteger:
    #         dynamicses = dynamics_pages.page(1)
    #     # 如果页数不存在/不合法，返回最后一页
    #     except InvalidPage:
    #         dynamicses = dynamics_pages.page(1)
    #     dynamicses_li = list(dynamicses.object_list.values())
    #     # 分别为是否有上一页false/true，是否有下一页false/true，总共多少页，当前页面的数据
    #     result = {'has_previous': dynamicses.has_previous(),
    #               'has_next': dynamicses.has_next(),
    #               'num_pages': dynamicses.paginator.num_pages,
    #               'dynamicses_li': dynamicses_li}
    #     return JsonResponse(result)


def edit_user_info(request, username):
    if not request.session.get('is_login', None):
        message = '还未登录，请登录后再访问！'
        url = '/login/'
        return render(request, 'buff.html', locals())
    username_1 = request.session.get('user_name')
    if username != username_1:
        message = '无效的页面，将返回首页！'
        url = '/index/'
        return render(request, 'buff.html', locals())
    # print(username, username_1)
    user = login.models.User.objects.get(username=username)
    # user_detail = login.models.UserDetail.objects.get(user=user)
    # user_detail_form = UserDetailForm()
    # user_detail_form.avatar = user_detail.avatar
    # user_detail_form.birthday = user_detail.birthday
    # user_detail_form.nickname = user_detail.nickname
    # user_detail_form.sex = user_detail.sex
    # user_detail_form.sign = user_detail.sign

    return render(request, 'user/edit_profile.html', locals())


def select_word(request):
    if not request.session.get('is_login', None):
        Login = False
        message = '还未登录，请登录后再访问！'
        url = '/login/'
        return render(request, 'buff.html', locals())
    username = request.session.get('user_name')
    try:
        user_word = UserWord.objects.get(username=username)
    except:
        user_word = UserWord()
        user_word.username = username
        user_word.word_type = 'cet-4'
        user_word.save()
    word_type = user_word.word_type
    return render(request, 'user/select_word.html', locals())


def select(request):
    if not request.session.get('is_login', None):
        data = {
            'status': 0, 'message': 'Please <a href="/login">Login</a> !', }
        return JsonResponse(data)

    if not request.is_ajax():
        data = {'status': 0, 'message': 'Maybe submit again?', }
        return JsonResponse(data)

    username = request.session.get('user_name')
    try:
        user_word = UserWord.objects.get(username=username)
    except:
        user_word = UserWord()
        user_word.username = username
    word_type = request.POST.get('type')
    user_word.word_type = word_type
    user_word.save()
    data = {'status': 1,
            'message': 'Change Success! Go to <a href="/check">learn</a> !'}
    dy = Dynamics()
    dy.add_dynamics(username, type="C", doing="change the word type for {}".format(word_type))
    return JsonResponse(data)


def ajax_get_user(request):
    if not request.is_ajax():
        return JsonResponse({'status': 0, 'message': 'Maybe have some error!'})
    if not request.session.get('is_login', None):
        return JsonResponse({'status': -1, 'message': 'Please login!'})
    username = request.session.get('user_name')
    user = login.models.User.objects.get(username=username)
    user_detail = login.models.UserDetail.objects.filter(user=user)
    if not user_detail:
        ud = login.models.UserDetail()
        ud.user = user
        ud.nickname = username + user.id
        ud.sex = 'other'
        ud.avatar = 'img/avatar.jpg'
        ud.save()
    else:
        ud = user_detail[0]

    return JsonResponse({'status': 1, 'avatar': str(ud.avatar), 'username': username,'nickname':ud.nickname, 'sign':ud.sign, 'birthday': str(ud.birthday), 'sex': str(ud.sex)})


def ajax_save(request):
    if not request.is_ajax():
        return JsonResponse({'status': 0, 'message': 'Maybe Request again?'})
    if not request.session.get('is_login', None):
        return JsonResponse({'status': 0, 'message': 'Please Login!'})

    # print(request.POST)
    username = request.session.get('user_name')
    user_0 = login.models.User.objects.get(username=username)
    user_detail = login.models.UserDetail.objects.get(user=user_0)

    uc = UserChange()
    uc.change_user = username
    uc.change_type = 'C'
    uc.save()
    cd = ChangeDetail()
    cd.change = uc
    cd.old_avatar = user_detail.avatar
    cd.old_nickname = user_detail.nickname
    cd.old_sign = user_detail.sign
    cd.old_sex = user_detail.sex
    cd.save()
    user_detail.nickname = request.POST.get('nickname')
    user_detail.sign = request.POST.get('sign')
    user_detail.sex = request.POST.get('radio_sex')
    user_detail.birthday = request.POST.get('birthday')
    try:
        img = request.FILES['img_file']
        user_detail.avatar = img
    except ( django.utils.datastructures.MultiValueDictKeyError) as e:
        print(e)
    user_detail.save()
    dynamics = Dynamics()
    dynamics.add_dynamics(username, type="C", doing="edit the profile")
    return JsonResponse({'status': 1, 'message': 'Change Success!', 'username': username})


def add_dynamics(username, type="O", target_id=1000,  doing="default"):
    # type R(random) 表示随机选择，L(letter) 表示首字母， N(Note) 表示Note，S(setence) 表示句子， C(change) 表示修改, M(mark) 表示收藏, F(finish)表示其它 O(other) 表示其它
    type = type.upper()
    user_0 = login.models.User.objects.filter(username=username)
    if not user_0:
        return False
    
    dynamics = Dynamics()
    dynamics.username = username
    dynamics.type = type
    dynamics.target_id = target_id
    if doing == 'default':
        if type == 'R':
            doing = 'create a new random check.'
        elif type == 'L':
            doing = 'create a new first letter check.'
        elif type == 'N':
            doing = 'create a new note.'
        elif type == 'S':
            doing = 'create a new Setence train.'
        elif type == 'C':
            doing = 'change user info.'
        elif type == 'F':
            doing = 'finish the check.'
        elif type == 'O':
            doing = 'maybe doing something.'

    dynamics.doing = doing
    dynamics.save()
    return True


        

    
