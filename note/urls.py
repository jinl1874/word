
from django.urls import path, re_path
from .views import edit_note, save_note,note

urlpatterns = [
    path('', note),
    path('save_note', save_note),
    re_path(r'(?P<note_id>[0-9]{3,5}?)/$', edit_note),
]