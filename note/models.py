from django.db import models


# Create your models here.
class Note(models.Model):
    id = models.AutoField(verbose_name='noteID', primary_key=True)
    username = models.CharField(max_length=64)
    title = models.CharField(max_length=512)
    content = models.TextField()
    t_time = models.DateTimeField(verbose_name='transform_time', auto_now=True)
    c_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)

    
    def __str__(self) -> str:
        return self.username + self.title
    
    class Meta:
        ordering = ['-c_time']
        verbose_name = 'Note'
        verbose_name_plural = "Notes"


class Mark(models.Model):
    note_id = models.IntegerField(verbose_name="noteID")
    username = models.CharField(max_length=64)
    c_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)

    def __str__(self) -> str:
        return self.username + 'mark: ' + str(self.note_id)

