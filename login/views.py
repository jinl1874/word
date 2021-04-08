import datetime
import hashlib
import pytz

from captcha.models import CaptchaStore
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render


from .form import *
# from django.shortcuts import render_to_response
from .models import *
import user.models


def ajax_val(request):
    if request.is_ajax():
        cs = CaptchaStore.objects.filter(
            response=request.GET['response'].lower(), hashkey=request.GET['hashkey'])
        if cs:
            json_data = {'status': 1}
            return JsonResponse(json_data)
        else:
            json_data = {'status': 0}
            return JsonResponse(json_data)
    else:
        json_data = {'status': 0}
        return JsonResponse(json_data)


def login(request):
    l_time = request.session.get('l_time', None)
    if l_time != None:
        l_time = datetime.datetime.strptime(l_time, '%Y-%m-%d %H:%M:%S')
        # 如果登录session超过30天, 就需要重新登录
        if datetime.datetime.now() > l_time + datetime.timedelta(30):
            request.session.flush()
    if request.session.get('is_login', None):
        # 不能重复登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = '验证码错误'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
            except:
                message = '用户不存在'
                return render(request, 'login/login.html', locals())
            if not user.has_confirmed:
                message = "该用户还未经过邮件确认！"
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                request.session['l_time'] = datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")
                record_ip(request, user.username)
                return redirect('/index/')
            else:
                message = '密码不正确'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = '验证码错误'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password_1 = register_form.cleaned_data.get('password1')
            password_2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            if password_1 != password_2:
                message = '两次输入的密码不同'
                return render(request, 'login/register.html', locals())
            if len(password_1) < 8:
                message = '输入的密码太短，密码至少8位'
                return render(request, 'login/register.html', locals())
            same_name_user = User.objects.filter(username=username)
            if same_name_user:
                message = '用户名已经存在'
                return render(request, 'login/register.html', locals())
            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                message = '该邮箱已经被注册'
                return render(request, 'login/register.html', locals())

            new_user = User()
            new_user.username = username
            new_user.password = hash_code(password_1)
            new_user.email = email
            new_user.save()

            code = make_confirm_string(new_user)
            send_email(email, code)
            message = '请往邮箱确认！'
            return render(request, 'login/confirm.html', locals())
        return render(request, 'login/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    # 如果没有登录的话，那就去登录吧
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    # 或者以下方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/login/')


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())
    c_time = confirm.c_time
    # 转人为可对比的时间
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "你的邮件已经过期！请重新注册！"
        return render(request, 'login/confirm.html', locals())
    confirm.user.has_confirmed = True
    confirm.user.save()
    confirm.delete()
    message = '感谢确认，请使用账户登录！'
    return render(request, 'login/confirm.html', locals())


def hash_code(s, salt='nyanpasu'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user: User):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code, type='R'):
    from django.core.mail import EmailMultiAlternatives
    if type == 'R':
        subject = '来自 悠哉网 的注册确认邮件'
        text_content = '''欢迎注册道理的悠哉网，这里是道理的各种笔记。
        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！
        '''
        html_content = '''
        <p> 感谢注册<a href="http://{}/confirm/?code={}" target=blank>jinl1874.xyz</a>的博客网站。</p>
        <p> 请点击站点链接完成注册确认！</p>
        <p> 此链接有效期为{}天</p>
        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    else:
        subject = '来自 悠哉网 的重置确认邮件'
        text_content = '''欢迎来到道理的悠哉网，这里是道理的各种笔记。
        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！
        '''
        html_content = '''
        <p><a href="http://{}/reset/?code={}" target=blank>link</a></p>
        <p> 请点击站点链接完成重置！</p>
        <p> 此链接有效期为{}天</p>
        '''.format('127.0.0.1:8000', code, 1)
    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def record_ip(request, username):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    lr = LoginRecord()
    lr.login_user = username
    lr.login_ip = ip
    lr.save()
    

def forget(request):
    status = 'fail'
    if request.method == 'POST':
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data.get('email')
            username = forget_form.cleaned_data.get('username')
            try:
                user = User.objects.get(email=email)
                user_1 = User.objects.get(username=username)
                if user.id != user_1.id:
                    message = '邮箱或用户错误，请重新输入'
                    return render(request, 'login/forget.html', locals())
            except:
                message = '邮箱或用户不存在，请重新输入'
                return render(request, 'login/forget.html', locals())
            
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            code = hash_code(user.username, now+'forget')
            ForgetString.objects.create(code=code, username=user.username)
            # send_email('email', code, type='F')
            message = '已经发送重置链接邮件到邮箱，请前往邮箱！'
            status = 'success'
            return render(request, 'login/forget.html', locals())
    forget_form = ForgetForm()
    return render(request, 'login/forget.html', locals())

def ajax_reset(request):
    if not request.is_ajax():
        data = {'status': 0, 'message': '也许重新点进来看下？',}
        return JsonResponse(data)
    reset_form = ResetForm()
    pwd = request.POST['password1']
    pwd_2 = request.POST['password2']
    code = request.POST['code']
    message = reset_form.check(pwd, pwd_2, code)
    if message != 'True':
        data = {
            'status': 0,
            'message': message,
        }
        return JsonResponse(data)
    pwd = hash_code(pwd)
    print(code)
    reset_form.save(pwd, code)
    message = '修改成功，请重新登录！'
    data = {
            'status': 1,
            'message': message,
    }
    return JsonResponse(data)
    


def reset(request):
    print("*"*18)
    # fail 失败，success 成功，
    status = 'fail'
    if request.method != "POST":
        reset_form = ResetForm()
        return render(request, 'login/reset.html', locals())
    # reset_form = ResetForm(request.POST)
    # if not reset_form.is_valid():
    #     message = '请检查输入'
    #     return render(request, 'login/reset.html', locals())

    # code = reset_form.cleaned_data.get('code')
    # try:
    #     forget_0 = ForgetString.objects.get(code=code)
    # except:
    #     message = "无效的重置密码请求，请前往邮箱查看！"
    #     return render(request, 'login/reset.html', locals())

    # c_time = forget_0.c_time
    # # 转人为可对比的时间
    # now = datetime.datetime.now()
    # now = now.replace(tzinfo=pytz.timezone('UTC'))
    # if now > c_time + datetime.timedelta(1):
    #     message = "你的邮件已经过期！请重新前往<a href='/forget/'>忘记密码</a>发送邮件！"
    #     return render(request, 'login/reset.html', locals())
    # p1 = reset_form.cleaned_data.get('password1')
    # p2 = reset_form.cleaned_data.get('password2')
    # if p1 != p2:
    #     message = '两次输入的密码不相同'
    #     return render(request, 'login/reset.html', locals())
    # if len(p1) < 8:
    #     message = '输入的密码长度太小，长度最小为8'
    #     return render(request, 'login/reset.html', locals())
    # user_0 = User.objects.get(username=forget_0.username)
    # hash_password = hash_code(p1)
    # pc = user.models.PasswordChange()
    # pc.change_user = user.username
    # pc.old_password = user.password
    # pc.new_password = hash_password
    # pc.save()
    # user.models.PasswordChange.objects.create(change_user=user.username, old_password=user.password, new_password=hash_password)
    # user.password = hash_password
    # user.save()

    # forget_0.delete()
    # message = '修改成功，请重新登录！'
    # request.session.flush()
    # status = 'success'
    # return render(request, 'login/reset.html', locals())
