from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', user),
    path('ajax_get_user', ajax_get_user),
    path('ajax_save', ajax_save),
    path('select', select),
    path('select_word/', select_word),
    re_path(r'(?P<username>[0-9a-zA-Z_-]+?)/edit/$', edit_user_info),
    re_path(r'(?P<username>[0-9a-zA-Z_-]+?)/$', user_info),
    re_path(r'(?P<username>[0-9a-zA-Z_-]+?)/edit/$', edit_user_info)
]
