from django.db import models
from django.db.models.lookups import Transform

# Create your models here.
class EnWords(models.Model):
    word = models.CharField(primary_key=True, max_length=64, unique=True, null=False, verbose_name='单词')
    translation = models.CharField(max_length=512, verbose_name='翻译')
    cet4 = models.BooleanField(verbose_name='四级')
    cet6 = models.BooleanField(verbose_name='六级')
    highschool = models.BooleanField(verbose_name='高中')
    other_type = models.CharField(max_length=128, verbose_name='其它类型')

    def __str__(self) -> str:
        return self.word

    class Meta:
        ordering = ['word']
        verbose_name = '单词'
        verbose_name_plural = '单词'

class EnSetence(models.Model):
    setence = models.CharField(max_length=512, verbose_name='句子')
    translation = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.setence[:64]

    class Meta:
        ordering = ['setence']
        verbose_name = '句子'
        verbose_name_plural = '句子'
