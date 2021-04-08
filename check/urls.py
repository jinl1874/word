from django.urls import path, re_path
from .views import check_num, check_word, ajax_type, ajax_save, check_result

urlpatterns = [
    path('', check_num),
    path('ajax_type', ajax_type),
    path('ajax_save', ajax_save),
    re_path(r'(?P<check_id>[0-9]{4,5}?)/result/$', check_result),
    re_path(r'(?P<check_id>[0-9]{4,5}?)/$', check_word),

]