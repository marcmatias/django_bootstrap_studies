from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'first_name', 'last_name', 'birthday', 'email']
    search_fields = ('first_name', 'email')
    # list_editable = ('name',)

admin.site.register(Contact, ContactAdmin)
