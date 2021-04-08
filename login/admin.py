from django.contrib import admin
from .models import *

# Register your models here.

class UserConfig(admin.ModelAdmin):
    # 显示的字段
    list_display = ('username', 'email', 'c_time')
    # 提供搜索的字段
    search_fields = ('username', 'email')
    # 根据日期过滤
    list_filter = ('c_time', )
    # 每页显示10
    list_per_page = 20
    # 根据register_date倒序显示
    ordering = ('-c_time', )


class DetailConfig(admin.ModelAdmin):
    list_display = ('user','nickname', 'sign')


class RecordConfig(admin.ModelAdmin):
    list_display = ('login_user','login_ip', 'login_time')

class ForgetConfig(admin.ModelAdmin):
    list_display = ('username', 'code', 'c_time')

admin.site.register(User, UserConfig)
admin.site.register(UserDetail, DetailConfig)
admin.site.register(ConfirmString)
admin.site.register(LoginRecord, RecordConfig)
admin.site.register(ForgetString, ForgetConfig)