from django.contrib import admin

# Register your models here.
from .models import Kb, Message, Category

admin.site.register(Kb)
admin.site.register(Message)
admin.site.register(Category)