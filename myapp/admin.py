from django.contrib import admin
from myapp.models import student



# Register your models here.

class studentadmin(admin.ModelAdmin):
    list_display = ('id','cName','cSex','cBirthday','cEmail','cPhone','cAdd')
    list_filter = ('cName','cSex')
    search_fields = ('cName',)
    #ordering = ('id',)

admin.site.register(student,studentadmin)
# Register your models here.
