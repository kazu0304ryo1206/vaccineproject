from django.contrib import admin
from .models import PlaceModel,CalendarModel,TimeModel,RegisterModel,CustomUser
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _ 
from django.utils.html import format_html


@admin.register(PlaceModel)
class PlaceModelAdmin(ImportExportModelAdmin):
    list_display = ['id','place','photo']
    def photo(self,obj):
        if obj.images:
            return format_html('<img src="{}" alt="画像" style="width:15rem">', obj.images.url)



class CalendarModelAdmin(ImportExportModelAdmin):
    list_display = ['id','day']


class TimeModelAdmin(ImportExportModelAdmin):
    list_display = ['id','time']


class RegisterModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','username','place','day','time','address','zip_code','age','check']
    #list_editable = ['check']
    ordering = ['place','day','-time']
    def address(self,obj):
        return obj.username.address.upper()
    def zip_code(self,obj):
        return obj.username.zip_code
    def age(self,obj):
        return obj.username.age
    address.short_description = '住所'
    #search_fields = ['time__time']
    """search_fields = ['check']
    fieldsets = (
        (_('Personal info'),{'fields':['check']}),
    )
    """

class CustomUserAdmin(UserAdmin,ImportExportModelAdmin):
    list_display = ['username','age','email','last_name','first_name','address','zip_code']
    empty_value_display = '-empty-'
    fieldsets = (
        (None,{'fields':('username','password')}),
        (_('Personal info'),{'fields':('first_name','last_name','email','age','address','zip_code')}),
        (_('Permissions'),{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        (_('Important dates'),{'fields':('last_login','date_joined')}),
    )

#admin.site.register(PlaceModel,PlaceModelAdmin)
admin.site.register(CalendarModel,CalendarModelAdmin)
admin.site.register(TimeModel,TimeModelAdmin)
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(RegisterModel,RegisterModelAdmin)
