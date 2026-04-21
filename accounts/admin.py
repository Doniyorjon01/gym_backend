from django.contrib import admin
from . import models, forms


class UserAdmin(admin.ModelAdmin):
    form = forms.UserForm
    list_display = ['phone_number', 'fullname', 'type', 'boss', 'email']
    list_filter = ['phone_number', 'fullname', 'type', 'email']
    search_fields = ['phone_number', 'fullname']


admin.site.register(models.User, UserAdmin)

