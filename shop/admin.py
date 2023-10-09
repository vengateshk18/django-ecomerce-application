from django.contrib import admin
from .models import *


class catagoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')
admin.site.register(Catagory,catagoryAdmin)
admin.site.register(Products)
# Register your models here.
