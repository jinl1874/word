from hashlib import new
from django.db import models
from django.db.models.deletion import CASCADE
import login.models


# Create your models here.
class UserChange(models.Model):
    change_user = models.CharField(max_length=128, verbose_name='修改用户')
    change_type = models.CharField(max_length=64, verbose_name='修改类型')
    change_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    def __str__(self) -> str:
        return self.change_user + ": " + str(self.change_time)

    class Meta:
        ordering = ['-change_time']
        verbose_name = '修改纪录'
        verbose_name_plural = "修改纪录"


class ChangeDetail(models.Model):
    change = models.OneToOneField(UserChange, on_delete=CASCADE)
    old_nickname = models.CharField(max_length=128, verbose_name='昵称')
    gender = (
        ('male', "男"),
        ('female', "女"),
        ('other', '其它')
    )
    old_sex = models.CharField(max_length=32, choices=gender)
    old_sign = models.CharField(
        max_length=256, verbose_name='签名')
    old_avatar = models.ImageField(upload_to='img', verbose_name='头像')

    def __str__(self) -> str:
        return self.change.change_user + ' ' + self.old_nickname


class PasswordChange(models.Model):
    change_user = models.CharField(max_length=128, verbose_name='修改用户')
    old_password = models.CharField(max_length=256, verbose_name='旧密码')
    new_password = models.CharField(max_length=256, verbose_name='新密码')
    change_time = models.TimeField(auto_now_add=True, verbose_name='修改时间')

    def __str__(self) -> str:
        return self.change_user

    class Meta:
        ordering = ['-change_time']
        verbose_name = '密码纪录'
        verbose_name_plural = "密码纪录"


class UserWord(models.Model):
    username = models.CharField(max_length=128, verbose_name='username')
    word_type = models.CharField(max_length=16, verbose_name='word_type')

    def __str__(self) -> str:
        return self.username + ': ' + self.word_type



class Dynamics(models.Model):
    username = models.CharField(max_length=128, verbose_name='username')
    doing = models.CharField(max_length=512, verbose_name='doing')
    target_id = models.IntegerField(verbose_name='target_id')
    type = models.CharField(max_length=2, verbose_name='type')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='time')
    def __str__(self) -> str:
        return self.username + ": " + self.doing[:20]

   
    def add_dynamics(self, username, type="O", target_id=1000,  doing="default"):
        # type R(random) 表示随机选择，L(letter) 表示首字母， N(Note) 表示Note，S(Star) 表示收藏， C(change) 表示修改,  F(finish)表示其它 O(other) 表示其它
        type = type.upper()
        user_0 = login.models.User.objects.filter(username=username)
        if not user_0:
            return False

        dynamics = Dynamics()
        self.username = username
        self.type = type
        self.target_id = target_id
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

        self.doing = doing
        self.save()
        return True