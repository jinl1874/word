from django.db import models

# Create your models here.
# Create your models here.
class Check(models.Model):
    # id, user, create_time, if_finish,
    id = models.AutoField(primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=64, verbose_name='用户名') 
    finish = models.BooleanField(verbose_name='if_finish')
    c_time = models.DateTimeField(auto_now_add=True)
    # last_edit = models.DateTimeField(auto_now=True)
    finish_time = models.DateTimeField(null=True, auto_now=True)
    # R 表示随机，L(random) 表示按首字母来选择
    type = models.CharField(verbose_name='CheckType', max_length=1, default='r')
    check_num = models.IntegerField(default=10)

    def __str__(self) -> str:
        return str(self.id) +  self.username 

    class Meta:
        ordering = ['-id']
        verbose_name = '检查纪录'
        verbose_name_plural = '检查纪录'


class CheckWordR(models.Model):
    # id, check, word time, if_do error_correct
    check_id = models.IntegerField(verbose_name='CheckID')
    username = models.CharField(max_length=64, verbose_name='用户名', default='null') 
    word = models.CharField(verbose_name='ENGWORD', max_length=20)
    result_word = models.CharField(verbose_name='ResultWord', max_length=20, default='')
    error_or_correct = models.BooleanField(null=True)
    if_do = models.BooleanField()
    

    def __str__(self) -> str:
        return str(self.check_id) + ": " +self.word

    class Meta:
        ordering = ['-check_id']
        verbose_name = '随机单词'
        verbose_name_plural = '随机单词'

class CheckWordL(models.Model):
    check_id = models.IntegerField(verbose_name='CheckID')
    username = models.CharField(max_length=64, verbose_name='用户名', default='null') 
    word = models.CharField(verbose_name='ENGWORD', max_length=20)
    result_word = models.CharField(verbose_name='ResultWord', max_length=20, default='')
    error_or_correct = models.BooleanField(null=True)
    if_do = models.BooleanField()
    letter = models.CharField(default='a', max_length=1)

    def __str__(self) -> str:
        return str(self.check_id) + ": " + self.word

    class Meta:
        ordering = ['-check_id']
        verbose_name = '首字母单词'
        verbose_name_plural = '首字母单词'

# class ErrorWord(models.Model):
class ResultWord(models.Model):
    check_id = models.IntegerField(verbose_name='CheckID')
    error_num = models.IntegerField(verbose_name='错误数')
    score = models.FloatField(verbose_name='Score')
    c_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.check_id) + ": " + str(self.score)

    class Meta:
        ordering = ['-c_time']
        verbose_name = '结果'
        verbose_name_plural = '结果'