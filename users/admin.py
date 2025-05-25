from django.contrib import admin
from .models import Users, UserAddress


admin.site.register(Users)
admin.site.register(UserAddress)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email') 
    search_fields = ('username', 'email')


class UsersAddress(admin.ModelAdmin):
    list_display = ('id', 'city', 'state') 
    search_fields = ('city', 'state')
