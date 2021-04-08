from re import T
from django.db import models
from django.db.models.deletion import CASCADE
from enum import Enum

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32,unique=True, null=False, verbose_name='用户名', db_index=True)
    password = models.CharField(max_length=256, null=False, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    has_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = "用户"

# 枚举类
# class SEX(Enum):
#     F = '女'
#     M = '男'
#     S = '保密'

class UserDetail(models.Model):
    user = models.OneToOneField('User', on_delete=CASCADE)
    nickname = models.CharField(max_length=128, default='喵帕斯', verbose_name='昵称')
    gender = (
        ('male', "男"),
        ('female', "女"),
        ('other', '其它')
    )
    sex = models.CharField(max_length=32, choices=gender, default='男')
    sign = models.CharField(
        max_length=256, verbose_name='签名', default='这个人很懒，什么也没有留下！')
    avatar = models.ImageField(upload_to='img', verbose_name='头像')
    birthday = models.DateField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.user.username + self.nickname

    class Meta:
        ordering = ['-last_edit']
        verbose_name = '用户信息'
        verbose_name_plural = "用户信息"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username + ": " + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = "确认码"


class LoginRecord(models.Model):
    login_user = models.CharField(max_length=128, verbose_name='用户')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    login_ip = models.CharField(max_length=31, verbose_name="IP")

    def __str__(self) -> str:
        return self.login_user

    class Meta:
        ordering = ['-login_time']
        verbose_name = '登录纪录'
        verbose_name_plural = "登录纪录"

class ForgetString(models.Model):
    code = models.CharField(max_length=256)
    username = models.CharField(max_length=128)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username + ": " + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '重置码'
        verbose_name_plural = "重置码"
