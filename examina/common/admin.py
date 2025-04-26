from django.contrib import admin
from .models import *

admin.site.register(institute)
admin.site.register(Contact)
@admin.register(HelpDeskTicket)
class HelpDeskTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at')
    search_fields = ('subject', 'name', 'email')
