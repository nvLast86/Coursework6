from django.contrib import admin

from mailing.models import Mailing, Contact, Message, MailingLog


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'contents')
    search_fields = ('header',)
    list_filter = ('header',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'periodicity', 'status', 'owner')
    search_fields = ('header', 'time')
    list_filter = ('time',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'owner')
    search_fields = ('last_name', 'email')
    list_filter = ('email',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'attempt', 'server_response')
    search_fields = ('time',)
    list_filter = ('time',)

