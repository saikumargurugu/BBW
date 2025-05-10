from django.contrib import admin
from .models import Organisation  # Adjust to your actual model name

admin.site.register(Organisation)

class orgnisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number')  # Customize fields
    search_fields = ('name', 'phone_number')
