from django.http.response import JsonResponse
from django.shortcuts import render
from .models import Note, Mark

# Create your views here.
def note(request):
    return render(request, 'note/edit_note.html')


def edit_note(request, note_id):
    note_li = Note.objects.filter(id=note_id)
    if not note_li:
        return render(request, 'error.html')
    note_0 = note_li[0]
    title = note_0.title
    content = note_0.content
    last_edit = note_0.c_time
    return render(request, 'note/edit_note.html', locals())



def save_note(request):
    return JsonResponse({})


def del_note(request):
    return JsonResponse({})


def mark(request):
    return JsonResponse({})