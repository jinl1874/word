from django.contrib import admin
from .models import *

# Register your models here.
# class WordConfig(admin.ModelAdmin):
#     list_display = ('word','translation')
#     search_fields = ('word','translation')

# class EnsetenceConfig(admin.ModelAdmin):
#     list_display = ('setence','translation')
#     search_fields = ('setence','translation')


admin.site.register(UserWord)
admin.site.register(UserChange)
admin.site.register(ChangeDetail)
admin.site.register(PasswordChange)
admin.site.register(Dynamics)