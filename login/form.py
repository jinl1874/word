from django import forms
from captcha import fields
from .models import *
import user.models
import datetime
import pytz


class UserForm(forms.Form):
    username = forms.CharField(label='用户', max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Username", 'autofocus': ''
    }))
    password = forms.CharField(
        label='密码', max_length=256, widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Password",
        }))
    captcha = fields.CaptchaField(label='验证码', widget=fields.CaptchaTextInput(attrs={
        'class': 'form-control',
    }))


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其它'),
    )
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "username",
    }))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "password",
    }))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={
        'placeholder': "confirm password",
        'class': 'form-control'
    }))
    email = forms.EmailField(label='邮箱地址', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': "email",
    }))
    # sex = forms.ChoiceField(label='性别', choices=gender, widget=forms.RadioSelect(attrs={
    #     'class': 'Radio'
    # }))
    captcha = fields.CaptchaField(label='验证码', widget=fields.CaptchaTextInput(attrs={
        'class': 'form-control',
        'placeholder': "captcha",
    }))


class ForgetForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "username",
    }))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': "email",
    }))


class ResetForm(forms.Form):
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "new_password",
    }))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "new_password",
    }))
    code = forms.CharField(label='code', max_length=256, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    def check(self, pwd1, pwd2, code):
        if code == 'None':
            message = '请去邮箱点击验证链接！'
            return message
        if len(pwd1) < 8 or len(pwd2) < 8:
            message = '密码的长度小于8！'
            return message
        if pwd1 != pwd2:
            message = '两次输入的密码不同！'
            return message
        try:
            forget_str = ForgetString.objects.get(code=code)
        except:
            message = "无效的重置密码请求，请前往邮箱查看！"
            return message

        c_time = forget_str.c_time
        # 转人为可对比的时间
        now = datetime.datetime.now()
        now = now.replace(tzinfo=pytz.timezone('UTC'))
        if now > c_time + datetime.timedelta(1):
            forget_str.delete()
            message = "你的邮件已经过期！请重新前往 <a href='/forget' class='alert-link'>忘记密码</a> 发送邮件！"
            return message

        return 'True'

    def save(self, password, code):
        forget_str = ForgetString.objects.get(code=code)
        user_0 = User.objects.get(username=forget_str.username)
        pc = user.models.PasswordChange()
        pc.change_user = user_0.username
        pc.old_password = user_0.password
        pc.new_password = password
        pc.save()

        user_0.password = password
        user_0.save()
