from django.contrib import admin
from .models import Users  # Adjust to your actual model name

admin.site.register(Users)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')  # Customize fields
    search_fields = ('username', 'email')
