from django.contrib import admin
from .models import Check, CheckWordL, CheckWordR, ResultWord

# Register your models here.
admin.site.register(Check)
admin.site.register(CheckWordR)
admin.site.register(CheckWordL)
admin.site.register(ResultWord)
